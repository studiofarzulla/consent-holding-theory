#!/usr/bin/env python3
"""
Generate publication-quality figures for Bayesian learning dynamics revision.
Creates three key figures:
1. Alpha convergence trajectories (all 5 mechanisms)
2. Friction reduction over time
3. Convergence speed comparison
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Publication-quality matplotlib settings
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 13,
    'lines.linewidth': 1.5,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# Define mechanism colors and labels
MECHANISMS = {
    'stakesweighted_docs': {'label': 'Stakes-Weighted DoCS', 'color': '#1f77b4'},
    'equal_voice': {'label': 'Equal Voice', 'color': '#ff7f0e'},
    'plutocracy': {'label': 'Plutocracy', 'color': '#d62728'},
    'expert_rule': {'label': 'Expert Rule', 'color': '#2ca02c'},
    'random_assignment': {'label': 'Random Assignment', 'color': '#9467bd'},
}

def load_data(mode='learning'):
    """Load all mechanism data for specified mode."""
    data = {}
    base_path = Path('/home/purrpower/Resurrexi/projects/need-work/consent-theory')

    for mech_key in MECHANISMS.keys():
        filename = f'dynamics_results_{mode}_{mech_key}.csv'
        filepath = base_path / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            data[mech_key] = df
        else:
            print(f"Warning: {filename} not found")

    return data

def compute_stats(df):
    """Compute mean and 95% CI across runs for each timestep."""
    grouped = df.groupby('timestep')['alpha'].agg(['mean', 'std', 'count'])
    grouped['ci_95'] = 1.96 * grouped['std'] / np.sqrt(grouped['count'])
    return grouped

def figure1_alpha_convergence():
    """Figure 1: Alpha trajectories with 95% CI for all mechanisms."""
    data = load_data('learning')

    fig, ax = plt.subplots(figsize=(10, 6))

    for mech_key, mech_data in MECHANISMS.items():
        if mech_key not in data:
            continue

        stats = compute_stats(data[mech_key])
        timesteps = stats.index

        # Plot mean line
        ax.plot(timesteps, stats['mean'],
                label=mech_data['label'],
                color=mech_data['color'],
                linewidth=2)

        # Plot 95% CI as shaded region
        ax.fill_between(timesteps,
                        stats['mean'] - stats['ci_95'],
                        stats['mean'] + stats['ci_95'],
                        color=mech_data['color'],
                        alpha=0.2)

    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Consent Alignment (α)', fontsize=12)
    ax.set_title('Consent Alignment Convergence Under Bayesian Learning', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 50)
    ax.set_ylim(0.4, 0.9)

    # Add annotation for DoCS final value
    if 'stakesweighted_docs' in data:
        final_alpha = compute_stats(data['stakesweighted_docs']).iloc[-1]['mean']
        ax.annotate(f'DoCS: α = {final_alpha:.3f}',
                   xy=(49, final_alpha), xytext=(42, final_alpha + 0.03),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1),
                   fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig('/home/purrpower/Resurrexi/projects/need-work/consent-theory/paper/figures/alpha_convergence_learning.pdf')
    print("Saved: alpha_convergence_learning.pdf")
    return fig

def figure2_friction_reduction():
    """Figure 2: Friction reduction over time for top 3 mechanisms."""
    data = load_data('learning')

    fig, ax = plt.subplots(figsize=(10, 6))

    # Focus on top 3 performers
    top_mechanisms = ['stakesweighted_docs', 'equal_voice', 'plutocracy']

    for mech_key in top_mechanisms:
        if mech_key not in data:
            continue

        mech_data = MECHANISMS[mech_key]
        df = data[mech_key]

        # Compute friction stats
        grouped = df.groupby('timestep')['friction'].agg(['mean', 'std', 'count'])
        grouped['ci_95'] = 1.96 * grouped['std'] / np.sqrt(grouped['count'])

        timesteps = grouped.index

        # Plot mean line
        ax.plot(timesteps, grouped['mean'],
                label=mech_data['label'],
                color=mech_data['color'],
                linewidth=2)

        # Plot 95% CI
        ax.fill_between(timesteps,
                        grouped['mean'] - grouped['ci_95'],
                        grouped['mean'] + grouped['ci_95'],
                        color=mech_data['color'],
                        alpha=0.2)

    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Friction (F)', fontsize=12)
    ax.set_title('Friction Reduction Under Bayesian Learning', fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 50)

    # Add annotation for DoCS friction reduction
    if 'stakesweighted_docs' in data:
        df_docs = data['stakesweighted_docs']
        initial_F = df_docs[df_docs['timestep'] == 0]['friction'].mean()
        final_F = df_docs[df_docs['timestep'] == 49]['friction'].mean()
        reduction_pct = 100 * (initial_F - final_F) / initial_F

        ax.text(25, ax.get_ylim()[1] * 0.85,
                f'DoCS friction reduction:\n{initial_F:.1f} → {final_F:.1f} (-{reduction_pct:.0f}%)',
                fontsize=10, bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', alpha=0.7))

    plt.tight_layout()
    plt.savefig('/home/purrpower/Resurrexi/projects/need-work/consent-theory/paper/figures/friction_reduction_learning.pdf')
    print("Saved: friction_reduction_learning.pdf")
    return fig

def figure3_convergence_speed():
    """Figure 3: Time to 90% of final alpha (bar chart)."""
    data = load_data('learning')

    convergence_times = {}

    for mech_key, df in data.items():
        # Compute final alpha (mean of last timestep across all runs)
        final_alpha = df[df['timestep'] == 49]['alpha'].mean()
        target_alpha = 0.9 * final_alpha

        # For each run, find first timestep where alpha >= target
        times = []
        for run_id in df['run'].unique():
            run_data = df[df['run'] == run_id].sort_values('timestep')
            converged = run_data[run_data['alpha'] >= target_alpha]
            if len(converged) > 0:
                times.append(converged.iloc[0]['timestep'])
            else:
                times.append(50)  # Didn't converge

        convergence_times[mech_key] = np.mean(times)

    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    mechanisms = list(convergence_times.keys())
    times = [convergence_times[m] for m in mechanisms]
    labels = [MECHANISMS[m]['label'] for m in mechanisms]
    colors = [MECHANISMS[m]['color'] for m in mechanisms]

    bars = ax.bar(labels, times, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{time:.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Time Periods to 90% Final α', fontsize=12)
    ax.set_title('Convergence Speed Comparison (Bayesian Learning)', fontsize=13, fontweight='bold')
    ax.set_ylim(0, max(times) * 1.15)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')

    plt.tight_layout()
    plt.savefig('/home/purrpower/Resurrexi/projects/need-work/consent-theory/paper/figures/convergence_speed_learning.pdf')
    print("Saved: convergence_speed_learning.pdf")
    return fig

def print_statistics():
    """Print key statistics for the paper."""
    data = load_data('learning')

    print("\n" + "="*60)
    print("KEY STATISTICS FOR PAPER REVISION")
    print("="*60)

    for mech_key, df in data.items():
        label = MECHANISMS[mech_key]['label']

        # Final alpha
        final_alpha = df[df['timestep'] == 49]['alpha'].mean()
        final_alpha_std = df[df['timestep'] == 49]['alpha'].std()

        # Initial alpha
        initial_alpha = df[df['timestep'] == 0]['alpha'].mean()

        # Alpha improvement
        improvement_pct = 100 * (final_alpha - initial_alpha) / initial_alpha

        # Final friction
        final_friction = df[df['timestep'] == 49]['friction'].mean()
        initial_friction = df[df['timestep'] == 0]['friction'].mean()
        friction_reduction_pct = 100 * (initial_friction - final_friction) / initial_friction

        # Monotonic convergence check
        monotonic_count = 0
        for run_id in df['run'].unique():
            run_data = df[df['run'] == run_id].sort_values('timestep')
            if (run_data['alpha'].diff().dropna() >= -0.001).all():  # Allow tiny decreases (numerical noise)
                monotonic_count += 1
        monotonic_pct = 100 * monotonic_count / df['run'].nunique()

        print(f"\n{label}:")
        print(f"  Final α: {final_alpha:.4f} (±{final_alpha_std:.4f})")
        print(f"  Initial α: {initial_alpha:.4f}")
        print(f"  Improvement: +{improvement_pct:.1f}%")
        print(f"  Final F: {final_friction:.2f}")
        print(f"  Friction reduction: -{friction_reduction_pct:.1f}%")
        print(f"  Monotonic runs: {monotonic_pct:.1f}%")

    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    print("Generating publication-quality figures for learning dynamics...\n")

    # Generate all figures
    figure1_alpha_convergence()
    figure2_friction_reduction()
    figure3_convergence_speed()

    # Print statistics
    print_statistics()

    print("\nAll figures generated successfully!")
    print("Location: /home/purrpower/Resurrexi/projects/need-work/consent-theory/paper/figures/")
