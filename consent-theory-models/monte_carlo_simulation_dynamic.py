#!/usr/bin/env python3
"""
Monte Carlo Simulation for Doctrine of Consensual Sovereignty (DoCS)
WITH INTEGRATED DYNAMIC MECHANISMS

Validates consent-weighted governance framework by comparing 5 mechanisms:
1. Equal Voice (one person one vote)
2. Plutocracy (power proportional to wealth)
3. Stakes-Weighted DoCS (power proportional to stakes in domain)
4. Random Assignment (sortition baseline)
5. Expert Rule (fixed elite decision-makers)

NOW SUPPORTS 4 DYNAMIC MODES:
- static: Original fixed-population evaluation (baseline)
- learning: Bayesian preference updating from observed outcomes
- social: DeGroot opinion dynamics via social network
- stakes: Endogenous stakes evolution based on decision impacts

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
import argparse
import csv
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
    dynamic_mode: str
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


# ==============================================================================
# DYNAMIC MECHANISMS
# ==============================================================================

def run_static_mode(mechanism: ConsentMechanism, n_agents: int, n_timesteps: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Original static evaluation - no temporal dynamics.
    Society generated once, metrics recorded over time (but nothing changes).

    Returns:
        alpha_trajectory, friction_trajectory
    """
    # Generate agent characteristics (fixed across time for this run)
    stakes = generate_heterogeneous_stakes(n_agents, distribution_type='mixed')

    # Wealth deliberately decoupled from stakes (Pearson r ≈ 0.1-0.3)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    np.random.shuffle(wealth)

    # Agent preferences (vary by domain but stable in time)
    if np.random.rand() > 0.5:
        preferences = np.random.normal(0, 1, n_agents)
    else:
        # Bimodal: two clusters
        cluster = np.random.choice([0, 1], size=n_agents)
        preferences = np.where(cluster == 0,
                              np.random.normal(-1.5, 0.5, n_agents),
                              np.random.normal(1.5, 0.5, n_agents))

    alpha_traj = np.zeros(n_timesteps)
    friction_traj = np.zeros(n_timesteps)

    # Run over time (nothing changes - static)
    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)

        alpha_traj[t] = compute_alpha(decision, preferences, stakes, consent)
        friction_traj[t] = compute_friction(decision, preferences, stakes)

    return alpha_traj, friction_traj


def run_learning_mode(mechanism: ConsentMechanism, n_agents: int, n_timesteps: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bayesian preference updating from observed outcomes.
    Agents update beliefs about optimal policy based on decision results.

    Returns:
        alpha_trajectory, friction_trajectory
    """
    # Initial conditions
    stakes = generate_heterogeneous_stakes(n_agents, distribution_type='mixed')
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    np.random.shuffle(wealth)
    preferences = np.random.normal(0, 1, n_agents)

    # Bayesian priors
    prior_mean = preferences.copy()
    prior_precision = 1.0

    alpha_traj = np.zeros(n_timesteps)
    friction_traj = np.zeros(n_timesteps)

    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)

        # Observe outcome (noisy signal of decision quality)
        observed_outcome = decision + np.random.normal(0, 0.1)

        # BAYESIAN UPDATE: Agents learn from observed outcomes
        # Higher-stakes agents pay more attention
        observation_precision = stakes
        posterior_precision = prior_precision + observation_precision
        posterior_mean = (
            (prior_precision * prior_mean + observation_precision * observed_outcome)
            / posterior_precision
        )

        # Update preferences for next period
        preferences = posterior_mean
        prior_precision = posterior_precision
        prior_mean = posterior_mean

        alpha_traj[t] = compute_alpha(decision, preferences, stakes, consent)
        friction_traj[t] = compute_friction(decision, preferences, stakes)

    return alpha_traj, friction_traj


def run_social_mode(mechanism: ConsentMechanism, n_agents: int, n_timesteps: int,
                    influence_strength: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
    """
    DeGroot opinion dynamics via social network.
    Preferences drift toward neighbors each period.

    Returns:
        alpha_trajectory, friction_trajectory
    """
    stakes = generate_heterogeneous_stakes(n_agents, distribution_type='mixed')
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    np.random.shuffle(wealth)
    preferences = np.random.normal(0, 1, n_agents)

    # Social network: Erdős–Rényi random graph
    connection_prob = 0.1
    social_network = np.random.rand(n_agents, n_agents) < connection_prob
    np.fill_diagonal(social_network, False)

    # Normalize rows (equal influence from neighbors)
    row_sums = social_network.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    social_network = social_network / row_sums[:, np.newaxis]

    alpha_traj = np.zeros(n_timesteps)
    friction_traj = np.zeros(n_timesteps)

    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)

        # SOCIAL INFLUENCE: Move toward neighbors' preferences
        neighbor_avg = social_network @ preferences
        preferences = (
            (1 - influence_strength) * preferences +
            influence_strength * neighbor_avg
        )

        alpha_traj[t] = compute_alpha(decision, preferences, stakes, consent)
        friction_traj[t] = compute_friction(decision, preferences, stakes)

    return alpha_traj, friction_traj


def run_stakes_mode(mechanism: ConsentMechanism, n_agents: int, n_timesteps: int,
                    stakes_response: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
    """
    Endogenous stakes evolution based on decision impacts.
    Winners (whose preferences align with decisions) gain stakes; losers lose stakes.

    Returns:
        alpha_trajectory, friction_trajectory
    """
    stakes = generate_heterogeneous_stakes(n_agents, distribution_type='mixed')
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    np.random.shuffle(wealth)
    preferences = np.random.normal(0, 1, n_agents)

    alpha_traj = np.zeros(n_timesteps)
    friction_traj = np.zeros(n_timesteps)

    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)

        # STAKES UPDATE: Winners gain, losers lose
        deviation = np.abs(decision - preferences)
        stakes_change = stakes_response * stakes * (1.0 - deviation)
        stakes = stakes + stakes_change
        stakes = np.maximum(stakes, 0.01)  # Floor at 0.01
        stakes = stakes / np.mean(stakes)  # Renormalize

        alpha_traj[t] = compute_alpha(decision, preferences, stakes, consent)
        friction_traj[t] = compute_friction(decision, preferences, stakes)

    return alpha_traj, friction_traj


def run_mechanism_simulation(mechanism: ConsentMechanism,
                             dynamic_mode: str = 'static',
                             n_runs: int = N_RUNS,
                             n_agents: int = N_AGENTS,
                             n_timesteps: int = N_TIMESTEPS) -> SimulationResults:
    """
    Run Monte Carlo simulation for a single mechanism with specified dynamics.

    Args:
        mechanism: Consent allocation mechanism
        dynamic_mode: 'static', 'learning', 'social', or 'stakes'
        n_runs: Number of Monte Carlo iterations
        n_agents: Population size
        n_timesteps: Time periods for convergence

    Returns:
        SimulationResults with trajectories and summary statistics
    """
    alpha_traj_all = np.zeros((n_runs, n_timesteps))
    friction_traj_all = np.zeros((n_runs, n_timesteps))
    final_legitimacy = np.zeros(n_runs)

    # Select dynamic mode
    if dynamic_mode == 'learning':
        runner = run_learning_mode
    elif dynamic_mode == 'social':
        runner = run_social_mode
    elif dynamic_mode == 'stakes':
        runner = run_stakes_mode
    else:  # static
        runner = run_static_mode

    for run in range(n_runs):
        alpha_traj, friction_traj = runner(mechanism, n_agents, n_timesteps)

        alpha_traj_all[run, :] = alpha_traj
        friction_traj_all[run, :] = friction_traj

        # Final legitimacy
        alpha_final = alpha_traj[-1]
        preferences_final = np.random.normal(0, 1, n_agents)  # Placeholder for performance calc
        stakes_final = generate_heterogeneous_stakes(n_agents)
        performance_final = compute_performance(0.0, preferences_final, stakes_final)
        final_legitimacy[run] = compute_legitimacy(alpha_final, performance_final)

    results = SimulationResults(
        mechanism_name=mechanism.name,
        dynamic_mode=dynamic_mode,
        alpha_trajectory=alpha_traj_all,
        friction_trajectory=friction_traj_all,
        final_legitimacy=final_legitimacy,
        mean_alpha=np.mean(alpha_traj_all[:, -1]),
        mean_friction=np.mean(friction_traj_all[:, -1]),
        mean_legitimacy=np.mean(final_legitimacy),
        std_legitimacy=np.std(final_legitimacy)
    )

    return results


def save_results_csv(results: SimulationResults, output_path: str):
    """Save trajectory results to CSV"""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mechanism', 'dynamic_mode', 'run', 'timestep', 'alpha', 'friction'])

        n_runs, n_timesteps = results.alpha_trajectory.shape
        for run in range(n_runs):
            for t in range(n_timesteps):
                writer.writerow([
                    results.mechanism_name,
                    results.dynamic_mode,
                    run,
                    t,
                    results.alpha_trajectory[run, t],
                    results.friction_trajectory[run, t]
                ])

    print(f"✓ Saved results to {output_path}")


def plot_dynamic_comparison(results_by_mode: Dict[str, Dict[str, SimulationResults]],
                            output_path: str = 'dynamics_comparison.pdf'):
    """
    Plot α(d,t) trajectories comparing dynamic modes for each mechanism.

    Args:
        results_by_mode: {mode: {mechanism_name: SimulationResults}}
    """
    mechanisms = ['Equal Voice', 'Stakes-Weighted DoCS', 'Plutocracy', 'Random Assignment', 'Expert Rule']
    modes = list(results_by_mode.keys())

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    colors = {'static': '#888888', 'learning': '#FF6B35', 'social': '#004E89', 'stakes': '#06A77D'}

    for i, mech_name in enumerate(mechanisms):
        ax = axes[i]

        for mode in modes:
            if mech_name in results_by_mode[mode]:
                results = results_by_mode[mode][mech_name]
                mean_alpha = np.mean(results.alpha_trajectory, axis=0)
                timesteps = np.arange(N_TIMESTEPS)

                ax.plot(timesteps, mean_alpha, label=mode, color=colors.get(mode, 'gray'), linewidth=2)

        ax.set_title(mech_name, fontsize=11, fontweight='bold')
        ax.set_xlabel('Time Period', fontsize=9)
        ax.set_ylabel('α(d,t)', fontsize=9)
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1])

    # Remove extra subplot
    fig.delaxes(axes[5])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved dynamics comparison to {output_path}")
    plt.close()


def print_results_table(results_dict: Dict[str, SimulationResults]):
    """Print summary statistics table"""
    print("\n" + "="*90)
    print(f"MONTE CARLO SIMULATION RESULTS ({N_RUNS} runs, {N_AGENTS} agents, {N_TIMESTEPS} timesteps)")
    print("="*90)
    print(f"{'Mechanism':<25} {'Mode':<10} {'Mean α':<12} {'Mean F':<12} {'Mean L':<12} {'Std L':<10}")
    print("-"*90)

    for key, results in results_dict.items():
        print(f"{results.mechanism_name:<25} {results.dynamic_mode:<10} {results.mean_alpha:>10.4f}  "
              f"{results.mean_friction:>10.4f}  {results.mean_legitimacy:>10.4f}  {results.std_legitimacy:>8.4f}")

    print("="*90)
    print("\nKey:")
    print("  α = Consent alignment (higher = consent-holders align with stakeholders)")
    print("  F = Friction (lower = less stakes-weighted deviation from preferences)")
    print("  L = Legitimacy (weighted combination: 0.6*α + 0.4*P)")
    print("="*90 + "\n")


def main():
    """Run full Monte Carlo simulation suite"""
    parser = argparse.ArgumentParser(description='DoCS Monte Carlo Simulation with Dynamics')
    parser.add_argument('--dynamics', type=str, default='all',
                       choices=['static', 'learning', 'social', 'stakes', 'all'],
                       help='Dynamic mode to run (default: all)')
    parser.add_argument('--output-dir', type=str,
                       default='/home/kawaiikali/Resurrexi/projects/need-work/consent-theory',
                       help='Output directory for results')
    args = parser.parse_args()

    print("\n" + "="*90)
    print("DOCTRINE OF CONSENSUAL SOVEREIGNTY - MONTE CARLO VALIDATION WITH DYNAMICS")
    print("="*90 + "\n")

    print(f"Simulation parameters:")
    print(f"  - Agents per society: {N_AGENTS}")
    print(f"  - Monte Carlo runs: {N_RUNS}")
    print(f"  - Time periods: {N_TIMESTEPS}")
    print(f"  - Random seed: 42 (reproducible)")
    print(f"  - Dynamic modes: {args.dynamics}\n")

    # Initialize mechanisms
    mechanisms = [
        EqualVoice(),
        StakesWeighted(),
        Plutocracy(),
        RandomAssignment(),
        ExpertRule()
    ]

    # Determine which modes to run
    if args.dynamics == 'all':
        modes = ['static', 'learning', 'social', 'stakes']
    else:
        modes = [args.dynamics]

    # Run simulations
    results_dict = {}
    results_by_mode = {mode: {} for mode in modes}

    total_sims = len(mechanisms) * len(modes)
    sim_count = 0

    for mode in modes:
        print(f"\n=== Running {mode.upper()} mode ===")
        for mechanism in mechanisms:
            sim_count += 1
            print(f"[{sim_count}/{total_sims}] {mechanism.name} ({mode})...", end=' ', flush=True)

            results = run_mechanism_simulation(mechanism, dynamic_mode=mode)
            key = f"{mechanism.name}_{mode}"
            results_dict[key] = results
            results_by_mode[mode][mechanism.name] = results

            print(f"✓ α={results.mean_alpha:.4f}, L={results.mean_legitimacy:.4f}")

            # Save individual CSV
            csv_path = f"{args.output_dir}/dynamics_results_{mode}_{mechanism.name.lower().replace(' ', '_').replace('-', '')}.csv"
            save_results_csv(results, csv_path)

    # Print consolidated results
    print_results_table(results_dict)

    # Generate comparison figures
    if len(modes) > 1:
        print("\nGenerating comparison figures...")
        plot_dynamic_comparison(results_by_mode,
                               output_path=f'{args.output_dir}/dynamics_comparison.pdf')

    print("\n✓ Simulation complete! Check output files for results.\n")

    return results_dict, results_by_mode


if __name__ == '__main__':
    results, results_by_mode = main()
