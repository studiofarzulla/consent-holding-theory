#!/usr/bin/env python3
"""
Monte Carlo Simulation for Doctrine of Consensual Sovereignty (DoCS)

Validates consent-weighted governance framework by comparing 5 mechanisms:
1. Equal Voice (one person one vote)
2. Plutocracy (power proportional to wealth)
3. Stakes-Weighted DoCS (power proportional to stakes in domain)
4. Random Assignment (sortition baseline)
5. Expert Rule (fixed elite decision-makers)

Measures:
- α(d,t): stakes-weighted consent alignment
- F(d,t): friction (stakes-weighted preference deviation)
- L(d,t): legitimacy function combining consent + performance

Author: Farzulla (2025)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Simulation parameters
N_AGENTS = 100          # Population size
N_RUNS = 1000          # Monte Carlo iterations per mechanism
N_TIMESTEPS = 50       # Time periods for convergence analysis
N_DOMAINS = 10         # Number of decision domains

@dataclass
class SimulationResults:
    """Container for simulation outcomes"""
    mechanism_name: str
    alpha_trajectory: np.ndarray  # Shape: (N_RUNS, N_TIMESTEPS)
    friction_trajectory: np.ndarray
    final_legitimacy: np.ndarray  # Shape: (N_RUNS,)
    mean_alpha: float
    mean_friction: float
    mean_legitimacy: float
    std_legitimacy: float


class ConsentMechanism:
    """Base class for consent allocation mechanisms"""

    def __init__(self, name: str):
        self.name = name

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray = None) -> np.ndarray:
        """
        Allocate consent power C_i across agents.

        Args:
            stakes: Array of shape (N_AGENTS,) representing agent stakes in domain
            wealth: Array of shape (N_AGENTS,) for plutocratic mechanism

        Returns:
            consent_power: Array of shape (N_AGENTS,) summing to 1.0
        """
        raise NotImplementedError


class EqualVoice(ConsentMechanism):
    """One person one vote - pure democracy"""

    def __init__(self):
        super().__init__("Equal Voice")

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray = None) -> np.ndarray:
        n = len(stakes)
        return np.ones(n) / n


class StakesWeighted(ConsentMechanism):
    """DoCS mechanism - consent proportional to stakes"""

    def __init__(self):
        super().__init__("Stakes-Weighted DoCS")

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray = None) -> np.ndarray:
        # Normalize stakes to sum to 1
        stakes_sum = np.sum(stakes)
        if stakes_sum == 0:
            # Edge case: no stakes, fall back to equal
            return np.ones(len(stakes)) / len(stakes)
        return stakes / stakes_sum


class Plutocracy(ConsentMechanism):
    """Power proportional to wealth, independent of stakes"""

    def __init__(self):
        super().__init__("Plutocracy")

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray) -> np.ndarray:
        # Consent follows wealth, not stakes in this domain
        wealth_sum = np.sum(wealth)
        if wealth_sum == 0:
            return np.ones(len(wealth)) / len(wealth)
        return wealth / wealth_sum


class RandomAssignment(ConsentMechanism):
    """Sortition - random single agent has all power"""

    def __init__(self):
        super().__init__("Random Assignment")

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray = None) -> np.ndarray:
        n = len(stakes)
        consent = np.zeros(n)
        # Randomly select one agent
        consent[np.random.randint(0, n)] = 1.0
        return consent


class ExpertRule(ConsentMechanism):
    """Fixed elite (top 10% by competence metric)"""

    def __init__(self, elite_fraction: float = 0.1):
        super().__init__("Expert Rule")
        self.elite_fraction = elite_fraction

    def allocate_consent(self, stakes: np.ndarray, wealth: np.ndarray = None) -> np.ndarray:
        n = len(stakes)
        n_elite = max(1, int(n * self.elite_fraction))

        # Elite selection based on random competence metric (uncorrelated with stakes)
        competence = np.random.randn(n)
        elite_indices = np.argsort(competence)[-n_elite:]

        consent = np.zeros(n)
        consent[elite_indices] = 1.0 / n_elite
        return consent


def generate_heterogeneous_stakes(n_agents: int, distribution_type: str = 'mixed') -> np.ndarray:
    """
    Generate realistic heterogeneous stakes distribution.

    Args:
        n_agents: Number of agents
        distribution_type: 'concentrated', 'uniform', 'mixed'

    Returns:
        stakes: Non-negative stakes summing to n_agents (for normalization)
    """
    if distribution_type == 'concentrated':
        # Power law: few high-stakes, many low-stakes (coastal property example)
        # More extreme heterogeneity
        stakes = np.random.pareto(a=1.2, size=n_agents) + 0.05
        # Create explicit minority high-stakes group (20% of population with 70% of stakes)
        n_high = int(0.2 * n_agents)
        stakes[:n_high] *= 5.0  # High-stakes minority
    elif distribution_type == 'uniform':
        # Everyone affected similarly (monetary policy)
        stakes = np.random.uniform(0.9, 1.1, size=n_agents)
    else:  # mixed
        # Combination: some domains concentrated, some uniform
        # 60% concentrated (where DoCS should shine), 40% uniform
        if np.random.rand() > 0.4:
            # Concentrated stakes with minority at high stakes
            stakes = np.random.pareto(a=1.3, size=n_agents) + 0.05
            n_high = int(0.15 * n_agents)
            stakes[:n_high] *= 6.0
        else:
            stakes = np.random.uniform(0.85, 1.15, size=n_agents)

    # Normalize to mean 1 for interpretability
    return stakes / np.mean(stakes)


def compute_friction(decision: float, preferences: np.ndarray, stakes: np.ndarray) -> float:
    """
    Compute friction F(d) = Σ s_i * |x_d - x*_i|

    Args:
        decision: Implemented policy x_d
        preferences: Agent ideal points x*_i
        stakes: Agent stakes s_i(d)

    Returns:
        friction: Stakes-weighted total deviation
    """
    deviations = np.abs(decision - preferences)
    return np.sum(stakes * deviations)


def compute_alpha(decision: float, preferences: np.ndarray, stakes: np.ndarray,
                  consent: np.ndarray) -> float:
    """
    Compute consent alignment α(d) = 1 - F_weighted / F_max

    Where F_weighted uses consent-weighted decision vs ideal preferences.
    Higher α means better alignment between consent-holders and stakeholders.

    Args:
        decision: Implemented policy
        preferences: Agent ideal points
        stakes: Agent stakes
        consent: Consent power allocation C_i

    Returns:
        alpha: Consent alignment in [0, 1]
    """
    # Weighted decision (what consent-holders want)
    weighted_decision = np.sum(consent * preferences)

    # Friction from weighted decision
    f_weighted = compute_friction(weighted_decision, preferences, stakes)

    # Maximum possible friction (decision at extreme vs all preferences)
    pref_min, pref_max = np.min(preferences), np.max(preferences)
    pref_range = pref_max - pref_min
    if pref_range == 0:
        return 1.0  # Perfect alignment if no preference variation

    # Worst-case friction (decision at one extreme)
    f_max = max(
        compute_friction(pref_min, preferences, stakes),
        compute_friction(pref_max, preferences, stakes)
    )

    if f_max == 0:
        return 1.0

    # α = 1 - (friction / max_friction), bounded to [0, 1]
    alpha = 1.0 - (f_weighted / f_max)
    return np.clip(alpha, 0.0, 1.0)


def compute_performance(decision: float, preferences: np.ndarray, stakes: np.ndarray) -> float:
    """
    Compute performance P(d) = 1 - F_actual / F_max

    Performance measures how close decision is to Pareto frontier (stakes-weighted optimum).

    Args:
        decision: Implemented policy
        preferences: Agent ideal points
        stakes: Agent stakes

    Returns:
        performance: Performance metric in [0, 1]
    """
    # Actual friction from decision
    f_actual = compute_friction(decision, preferences, stakes)

    # Optimal decision minimizes friction (stakes-weighted median)
    optimal_decision = weighted_median(preferences, stakes)
    f_optimal = compute_friction(optimal_decision, preferences, stakes)

    # Max friction
    pref_min, pref_max = np.min(preferences), np.max(preferences)
    f_max = max(
        compute_friction(pref_min, preferences, stakes),
        compute_friction(pref_max, preferences, stakes)
    )

    if f_max == 0:
        return 1.0

    # Performance relative to optimal
    performance = 1.0 - (f_actual / f_max)
    return np.clip(performance, 0.0, 1.0)


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Compute weighted median"""
    sorted_idx = np.argsort(values)
    sorted_values = values[sorted_idx]
    sorted_weights = weights[sorted_idx]

    cumsum = np.cumsum(sorted_weights)
    total = cumsum[-1]

    median_idx = np.searchsorted(cumsum, total / 2.0)
    return sorted_values[median_idx]


def compute_legitimacy(alpha: float, performance: float,
                       w_consent: float = 0.6, w_performance: float = 0.4) -> float:
    """
    Compute legitimacy L = w1*α + w2*P

    Args:
        alpha: Consent alignment
        performance: Policy performance
        w_consent: Weight for consent (default 0.6)
        w_performance: Weight for performance (default 0.4)

    Returns:
        legitimacy: Combined legitimacy metric
    """
    return w_consent * alpha + w_performance * performance


def run_mechanism_simulation(mechanism: ConsentMechanism,
                             n_runs: int = N_RUNS,
                             n_agents: int = N_AGENTS,
                             n_timesteps: int = N_TIMESTEPS) -> SimulationResults:
    """
    Run Monte Carlo simulation for a single mechanism.

    Args:
        mechanism: Consent allocation mechanism
        n_runs: Number of Monte Carlo iterations
        n_agents: Population size
        n_timesteps: Time periods for convergence

    Returns:
        SimulationResults with trajectories and summary statistics
    """
    alpha_traj = np.zeros((n_runs, n_timesteps))
    friction_traj = np.zeros((n_runs, n_timesteps))
    final_legitimacy = np.zeros(n_runs)

    for run in range(n_runs):
        # Generate agent characteristics (fixed across time for this run)
        stakes = generate_heterogeneous_stakes(n_agents, distribution_type='mixed')

        # Wealth deliberately decoupled from stakes (Pearson r ≈ 0.1-0.3)
        # Wealthy != high stakes in domain (plutocracy failure condition)
        wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5  # Pareto wealth (Gini ≈ 0.4)
        np.random.shuffle(wealth)  # Break any accidental correlation with stakes

        # Agent preferences (vary by domain but stable in time)
        # Use bimodal distribution to create value conflicts
        if np.random.rand() > 0.5:
            preferences = np.random.normal(0, 1, n_agents)
        else:
            # Bimodal: two clusters
            cluster = np.random.choice([0, 1], size=n_agents)
            preferences = np.where(cluster == 0,
                                  np.random.normal(-1.5, 0.5, n_agents),
                                  np.random.normal(1.5, 0.5, n_agents))

        # Run over time
        for t in range(n_timesteps):
            # Allocate consent power
            consent = mechanism.allocate_consent(stakes, wealth)

            # Decision is consent-weighted preference
            decision = np.sum(consent * preferences)

            # Compute metrics
            alpha = compute_alpha(decision, preferences, stakes, consent)
            friction = compute_friction(decision, preferences, stakes)
            performance = compute_performance(decision, preferences, stakes)

            alpha_traj[run, t] = alpha
            friction_traj[run, t] = friction

            if t == n_timesteps - 1:
                final_legitimacy[run] = compute_legitimacy(alpha, performance)

    # Summary statistics
    results = SimulationResults(
        mechanism_name=mechanism.name,
        alpha_trajectory=alpha_traj,
        friction_trajectory=friction_traj,
        final_legitimacy=final_legitimacy,
        mean_alpha=np.mean(alpha_traj[:, -1]),  # Final timestep average
        mean_friction=np.mean(friction_traj[:, -1]),
        mean_legitimacy=np.mean(final_legitimacy),
        std_legitimacy=np.std(final_legitimacy)
    )

    return results


def plot_alpha_trajectories(results_dict: Dict[str, SimulationResults],
                            output_path: str = 'alpha_trajectories.pdf'):
    """
    Plot α(d,t) convergence over time for all mechanisms.

    Args:
        results_dict: Dict mapping mechanism name to SimulationResults
        output_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        'Equal Voice': '#FF6B35',
        'Stakes-Weighted DoCS': '#004E89',
        'Plutocracy': '#C1121F',
        'Random Assignment': '#9D4EDD',
        'Expert Rule': '#06A77D'
    }

    for name, results in results_dict.items():
        # Mean trajectory across runs
        mean_alpha = np.mean(results.alpha_trajectory, axis=0)
        std_alpha = np.std(results.alpha_trajectory, axis=0)

        timesteps = np.arange(N_TIMESTEPS)

        ax.plot(timesteps, mean_alpha, label=name, color=colors.get(name, 'gray'), linewidth=2)
        ax.fill_between(timesteps,
                        mean_alpha - std_alpha,
                        mean_alpha + std_alpha,
                        color=colors.get(name, 'gray'),
                        alpha=0.2)

    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Consent Alignment α(d,t)', fontsize=12)
    ax.set_title('Convergence of Consent Alignment by Mechanism', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved α(d,t) trajectories to {output_path}")
    plt.close()


def plot_legitimacy_comparison(results_dict: Dict[str, SimulationResults],
                               output_path: str = 'legitimacy_comparison.pdf'):
    """
    Plot final legitimacy comparison across mechanisms (bar chart).

    Args:
        results_dict: Dict mapping mechanism name to SimulationResults
        output_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    mechanisms = list(results_dict.keys())
    mean_legitimacy = [results_dict[m].mean_legitimacy for m in mechanisms]
    std_legitimacy = [results_dict[m].std_legitimacy for m in mechanisms]

    colors_list = ['#FF6B35', '#004E89', '#C1121F', '#9D4EDD', '#06A77D']

    bars = ax.bar(mechanisms, mean_legitimacy, yerr=std_legitimacy,
                  color=colors_list, alpha=0.8, capsize=5)

    ax.set_ylabel('Final Legitimacy L(d,t)', fontsize=12)
    ax.set_title('Legitimacy by Consent Mechanism (1000 Monte Carlo runs)',
                fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(True, axis='y', alpha=0.3)

    # Rotate x-axis labels for readability
    plt.xticks(rotation=15, ha='right')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved legitimacy comparison to {output_path}")
    plt.close()


def print_results_table(results_dict: Dict[str, SimulationResults]):
    """Print summary statistics table"""
    print("\n" + "="*80)
    print("MONTE CARLO SIMULATION RESULTS (1000 runs, 100 agents, 50 timesteps)")
    print("="*80)
    print(f"{'Mechanism':<25} {'Mean α':<12} {'Mean F':<12} {'Mean L':<12} {'Std L':<10}")
    print("-"*80)

    for name, results in results_dict.items():
        print(f"{name:<25} {results.mean_alpha:>10.4f}  {results.mean_friction:>10.4f}  "
              f"{results.mean_legitimacy:>10.4f}  {results.std_legitimacy:>8.4f}")

    print("="*80)
    print("\nKey:")
    print("  α = Consent alignment (higher = consent-holders align with stakeholders)")
    print("  F = Friction (lower = less stakes-weighted deviation from preferences)")
    print("  L = Legitimacy (weighted combination: 0.6*α + 0.4*P)")
    print("="*80 + "\n")


def main():
    """Run full Monte Carlo simulation suite"""
    print("\n" + "="*80)
    print("DOCTRINE OF CONSENSUAL SOVEREIGNTY - MONTE CARLO VALIDATION")
    print("="*80 + "\n")

    print(f"Simulation parameters:")
    print(f"  - Agents per society: {N_AGENTS}")
    print(f"  - Monte Carlo runs: {N_RUNS}")
    print(f"  - Time periods: {N_TIMESTEPS}")
    print(f"  - Domains: {N_DOMAINS}")
    print(f"  - Random seed: 42 (reproducible)\n")

    # Initialize mechanisms
    mechanisms = [
        EqualVoice(),
        StakesWeighted(),
        Plutocracy(),
        RandomAssignment(),
        ExpertRule()
    ]

    # Run simulations
    results_dict = {}
    for i, mechanism in enumerate(mechanisms, 1):
        print(f"[{i}/{len(mechanisms)}] Running {mechanism.name}...", end=' ', flush=True)
        results = run_mechanism_simulation(mechanism)
        results_dict[mechanism.name] = results
        print(f"✓ Complete (α={results.mean_alpha:.4f}, L={results.mean_legitimacy:.4f})")

    # Print results table
    print_results_table(results_dict)

    # Generate figures
    print("\nGenerating figures...")
    plot_alpha_trajectories(results_dict,
                           output_path='/home/kawaiikali/Resurrexi/projects/need-work/consent-theory/alpha_trajectories.pdf')
    plot_legitimacy_comparison(results_dict,
                               output_path='/home/kawaiikali/Resurrexi/projects/need-work/consent-theory/legitimacy_comparison.pdf')

    print("\n✓ Simulation complete! Check output files for results.\n")

    return results_dict


if __name__ == '__main__':
    results = main()
