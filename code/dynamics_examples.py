#!/usr/bin/env python3
"""
Example: How to implement ACTUAL dynamics in the DoCS simulation

This shows three minimal dynamic mechanisms that would produce genuine convergence:
1. Preference learning from past decisions
2. Social influence on preference formation  
3. Endogenous stakes evolution based on decision impacts
"""

import numpy as np

# ==============================================================================
# OPTION 1: BAYESIAN PREFERENCE UPDATING
# ==============================================================================

def run_with_preference_learning(mechanism, n_agents=100, n_timesteps=50):
    """
    Agents update preferences based on observed decision outcomes.
    
    Logic: After seeing decision[t], agents update beliefs about optimal policy
    via Bayesian learning. This creates genuine temporal dynamics.
    """
    
    # Initial conditions (same as before)
    stakes = generate_heterogeneous_stakes(n_agents)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    preferences = np.random.normal(0, 1, n_agents)  # Initial beliefs
    
    # Priors: agents think true optimum is distributed around their initial preference
    prior_mean = preferences.copy()
    prior_precision = 1.0  # Certainty about initial belief
    
    alpha_trajectory = np.zeros(n_timesteps)
    
    for t in range(n_timesteps):
        # Current consent allocation
        consent = mechanism.allocate_consent(stakes, wealth)
        
        # Implemented decision
        decision = np.sum(consent * preferences)
        
        # Observe outcome quality (simplified: distance from decision)
        # In reality, this would be observed welfare, social outcomes, etc.
        observed_outcome = decision + np.random.normal(0, 0.1)  # Noisy signal
        
        # BAYESIAN UPDATE: Agents update preferences toward observed outcome
        # Higher-stakes agents weight observations more heavily (they pay attention)
        observation_precision = stakes  # High stakes → pay more attention
        
        # Posterior becomes next period's prior
        posterior_precision = prior_precision + observation_precision
        posterior_mean = (
            (prior_precision * prior_mean + observation_precision * observed_outcome) 
            / posterior_precision
        )
        
        # Update for next period
        preferences = posterior_mean
        prior_precision = posterior_precision
        prior_mean = posterior_mean
        
        # Measure current alignment
        alpha_trajectory[t] = compute_alpha(decision, preferences, stakes, consent)
    
    return alpha_trajectory


# ==============================================================================
# OPTION 2: SOCIAL INFLUENCE DYNAMICS
# ==============================================================================

def run_with_social_influence(mechanism, n_agents=100, n_timesteps=50, 
                               influence_strength=0.1):
    """
    Preferences influenced by social network (DeGroot-style opinion dynamics).
    
    Logic: Each agent's preference moves toward neighbors' preferences each period.
    Creates convergence to consensus or polarization depending on network structure.
    """
    
    stakes = generate_heterogeneous_stakes(n_agents)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    preferences = np.random.normal(0, 1, n_agents)
    
    # Social network: random graph (Erdős–Rényi)
    connection_prob = 0.1
    social_network = np.random.rand(n_agents, n_agents) < connection_prob
    np.fill_diagonal(social_network, False)  # No self-loops
    
    # Normalize rows (each agent's neighbors have equal influence)
    row_sums = social_network.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero for isolated agents
    social_network = social_network / row_sums[:, np.newaxis]
    
    alpha_trajectory = np.zeros(n_timesteps)
    
    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)
        
        # SOCIAL INFLUENCE: Move toward neighbors' preferences
        neighbor_avg = social_network @ preferences  # Matrix multiplication
        preferences_new = (
            (1 - influence_strength) * preferences + 
            influence_strength * neighbor_avg
        )
        
        preferences = preferences_new
        
        alpha_trajectory[t] = compute_alpha(decision, preferences, stakes, consent)
    
    return alpha_trajectory


# ==============================================================================
# OPTION 3: ENDOGENOUS STAKES EVOLUTION
# ==============================================================================

def run_with_stakes_evolution(mechanism, n_agents=100, n_timesteps=50,
                               stakes_response=0.05):
    """
    Stakes evolve based on decision impacts (winners accumulate stakes).
    
    Logic: Agents whose preferences align with decisions gain stakes;
    those far from decisions lose stakes. Creates winner-take-all dynamics
    or convergence depending on parameters.
    """
    
    stakes = generate_heterogeneous_stakes(n_agents)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    preferences = np.random.normal(0, 1, n_agents)
    
    alpha_trajectory = np.zeros(n_timesteps)
    
    for t in range(n_timesteps):
        consent = mechanism.allocate_consent(stakes, wealth)
        decision = np.sum(consent * preferences)
        
        # STAKES UPDATE: Winners gain, losers lose
        # Distance from decision determines gain/loss
        deviation = np.abs(decision - preferences)
        stakes_change = stakes_response * stakes * (1.0 - deviation)
        
        # Update stakes (with floor to prevent negative)
        stakes = stakes + stakes_change
        stakes = np.maximum(stakes, 0.01)  # Floor at 0.01
        
        # Renormalize to prevent unbounded growth
        stakes = stakes / np.mean(stakes)
        
        alpha_trajectory[t] = compute_alpha(decision, preferences, stakes, consent)
    
    return alpha_trajectory


# ==============================================================================
# OPTION 4: ADAPTIVE CONSENT MECHANISMS
# ==============================================================================

def run_with_adaptive_mechanism(n_agents=100, n_timesteps=50, learning_rate=0.01):
    """
    Mechanism itself learns from friction history.
    
    Logic: Consent allocation adapts to minimize observed friction over time.
    Meta-learning at the institutional level.
    """
    
    stakes = generate_heterogeneous_stakes(n_agents)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    preferences = np.random.normal(0, 1, n_agents)
    
    # Initialize consent allocation (start with equal voice)
    consent = np.ones(n_agents) / n_agents
    
    alpha_trajectory = np.zeros(n_timesteps)
    friction_history = []
    
    for t in range(n_timesteps):
        # Current decision
        decision = np.sum(consent * preferences)
        
        # Measure friction
        friction = compute_friction(decision, preferences, stakes)
        friction_history.append(friction)
        
        # ADAPTIVE MECHANISM: Gradient descent on friction
        # Increase consent for agents whose preferences align with reducing friction
        gradient = np.zeros(n_agents)
        for i in range(n_agents):
            # Perturb consent[i] and measure friction change
            consent_perturbed = consent.copy()
            consent_perturbed[i] += 0.001
            consent_perturbed /= consent_perturbed.sum()  # Renormalize
            
            decision_perturbed = np.sum(consent_perturbed * preferences)
            friction_perturbed = compute_friction(decision_perturbed, preferences, stakes)
            
            gradient[i] = -(friction_perturbed - friction)  # Negative gradient
        
        # Update consent allocation
        consent = consent + learning_rate * gradient
        consent = np.maximum(consent, 0)  # Non-negativity
        consent = consent / consent.sum()  # Normalize
        
        alpha_trajectory[t] = compute_alpha(decision, preferences, stakes, consent)
    
    return alpha_trajectory


# ==============================================================================
# OPTION 5: ENTRY/EXIT DYNAMICS
# ==============================================================================

def run_with_entry_exit(mechanism, n_agents=100, n_timesteps=50, 
                        exit_threshold=-0.5):
    """
    Agents exit system if satisfaction drops below threshold.
    
    Logic: Dissatisfied agents leave (emigration, withdrawal, non-participation).
    Creates selection effects and potential death spirals or stabilization.
    """
    
    stakes = generate_heterogeneous_stakes(n_agents)
    wealth = np.random.pareto(a=1.16, size=n_agents) + 0.5
    preferences = np.random.normal(0, 1, n_agents)
    
    # Initial: everyone active
    active = np.ones(n_agents, dtype=bool)
    satisfaction = np.zeros(n_agents)
    
    alpha_trajectory = np.zeros(n_timesteps)
    
    for t in range(n_timesteps):
        # Only active agents participate
        if active.sum() == 0:
            break  # System collapsed
        
        stakes_active = stakes[active]
        wealth_active = wealth[active]
        preferences_active = preferences[active]
        
        consent_active = mechanism.allocate_consent(stakes_active, wealth_active)
        decision = np.sum(consent_active * preferences_active)
        
        # Update satisfaction for active agents
        deviation = np.abs(decision - preferences_active)
        satisfaction[active] = satisfaction[active] * 0.9 - deviation  # Exponential decay
        
        # EXIT DECISION: Leave if satisfaction too low
        active[active] = satisfaction[active] > exit_threshold
        
        # Measure alignment among remaining population
        if active.sum() > 0:
            alpha_trajectory[t] = compute_alpha(
                decision, preferences_active, stakes_active, consent_active
            )
        else:
            alpha_trajectory[t] = 0.0  # System collapsed
    
    return alpha_trajectory


# ==============================================================================
# HELPER FUNCTIONS (same as your original code)
# ==============================================================================

def generate_heterogeneous_stakes(n_agents, distribution_type='mixed'):
    """Your original function"""
    if distribution_type == 'mixed':
        if np.random.rand() > 0.4:
            stakes = np.random.pareto(a=1.3, size=n_agents) + 0.05
            n_high = int(0.15 * n_agents)
            stakes[:n_high] *= 6.0
        else:
            stakes = np.random.uniform(0.85, 1.15, size=n_agents)
    return stakes / np.mean(stakes)


def compute_friction(decision, preferences, stakes):
    """Your original function"""
    deviations = np.abs(decision - preferences)
    return np.sum(stakes * deviations)


def compute_alpha(decision, preferences, stakes, consent):
    """Your original function (simplified version)"""
    weighted_decision = np.sum(consent * preferences)
    f_weighted = compute_friction(weighted_decision, preferences, stakes)
    
    pref_range = np.max(preferences) - np.min(preferences)
    if pref_range == 0:
        return 1.0
    
    f_max = max(
        compute_friction(np.max(preferences), preferences, stakes),
        compute_friction(np.min(preferences), preferences, stakes)
    )
    
    if f_max == 0:
        return 1.0
    
    return 1.0 - (f_weighted / f_max)


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == '__main__':
    print("Example: Implementing real dynamics in DoCS simulation")
    print("="*60)
    print()
    
    # Run with different dynamic mechanisms
    print("Option 1: Bayesian preference learning")
    alpha_learning = run_with_preference_learning(
        mechanism=StakesWeighted(), 
        n_timesteps=50
    )
    print(f"  Initial α = {alpha_learning[0]:.4f}")
    print(f"  Final α   = {alpha_learning[-1]:.4f}")
    print(f"  Change    = {alpha_learning[-1] - alpha_learning[0]:.4f}")
    print()
    
    print("Option 2: Social influence")
    alpha_social = run_with_social_influence(
        mechanism=StakesWeighted(),
        n_timesteps=50,
        influence_strength=0.1
    )
    print(f"  Initial α = {alpha_social[0]:.4f}")
    print(f"  Final α   = {alpha_social[-1]:.4f}")
    print(f"  Change    = {alpha_social[-1] - alpha_social[0]:.4f}")
    print()
    
    print("Notice: Trajectories now actually CHANGE over time!")
    print("This is genuine convergence, not Monte Carlo noise.")
