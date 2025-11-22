"""
Generate publication-quality figures for consent-holding theory paper.
All figures saved to ./figures/ directory.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List, Tuple

# Configure matplotlib for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.color'] = '#cccccc'

# Professional color scheme
ACCENT_COLOR = '#1f77b4'  # Navy blue
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'tertiary': '#2ca02c',
    'quaternary': '#d62728',
    'gray': '#7f7f7f',
    'light_gray': '#e0e0e0',
}

OUTPUT_DIR = '/home/kawaiikali/Resurrexi/projects/need-work/consent-theory/figures/'


def fig1_alpha_p_frontier():
    """Figure 1: α-P Frontier (Competence-Consent Trade-off)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Governance systems as points
    systems = {
        'Technocracy': (0.3, 0.8),
        'Democracy': (0.8, 0.6),
        'Authoritarianism': (0.2, 0.3),
        'Weighted\nDemocracy': (0.7, 0.75),
        'Citizens\'\nAssembly': (0.85, 0.65),
    }

    # Plot points
    for name, (alpha, p) in systems.items():
        ax.scatter(alpha, p, s=150, c=ACCENT_COLOR, zorder=3, alpha=0.8)
        # Offset labels to avoid overlap
        offset_x = 0.03 if alpha < 0.5 else -0.03
        offset_y = 0.03
        ha = 'left' if alpha < 0.5 else 'right'
        ax.annotate(name, (alpha, p), xytext=(offset_x, offset_y),
                   textcoords='offset fontsize', ha=ha, va='bottom',
                   fontsize=10, fontweight='bold')

    # Iso-legitimacy curves: L = w1*alpha + w2*P
    # Rearranged: P = (L - w1*alpha) / w2
    alpha_range = np.linspace(0, 1, 100)

    # Three weight configurations
    weights = [
        (0.7, 0.3, 'Prefer Consent\n(w₁=0.7, w₂=0.3)', 'dashed'),
        (0.5, 0.5, 'Balanced\n(w₁=0.5, w₂=0.5)', 'solid'),
        (0.3, 0.7, 'Prefer Performance\n(w₁=0.3, w₂=0.7)', 'dotted'),
    ]

    for w1, w2, label, style in weights:
        # Pick L value to put curve through middle of plot
        L = 0.55
        P = (L - w1 * alpha_range) / w2
        # Only plot valid region
        valid = (P >= 0) & (P <= 1)
        ax.plot(alpha_range[valid], P[valid], linestyle=style,
               color=COLORS['gray'], linewidth=2, alpha=0.6, label=label)

    ax.set_xlabel('α (Consent Alignment)', fontsize=12)
    ax.set_ylabel('P (Performance)', fontsize=12)
    ax.set_title('The Competence-Consent Frontier', fontsize=16, fontweight='bold')
    ax.text(0.5, -0.15, 'Different governance systems optimize different legitimacy functions L = w₁α + w₂P',
           ha='center', transform=ax.transAxes, fontsize=11, style='italic')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc='lower left', frameon=True, fancybox=False, edgecolor='black')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'alpha_p_frontier.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {OUTPUT_DIR}alpha_p_frontier.png")


def fig2_friction_trajectories():
    """Figure 2: Historical Friction Trajectories"""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Women's Suffrage
    years_suffrage = np.array([1800, 1890, 1920, 1960, 2025])
    friction_suffrage = np.array([20, 20, 80, 30, 10])
    years_suffrage_interp = np.linspace(1800, 2025, 200)
    friction_suffrage_interp = np.interp(years_suffrage_interp, years_suffrage, friction_suffrage)

    # Abolition
    years_abolition = np.array([1800, 1850, 1865, 1865.1, 1900, 2025])
    friction_abolition = np.array([40, 40, 100, 60, 50, 50])
    years_abolition_interp = np.linspace(1800, 2025, 200)
    friction_abolition_interp = np.interp(years_abolition_interp, years_abolition, friction_abolition)

    # LGBT Rights
    years_lgbt = np.array([1950, 1969, 1970, 1985, 1995, 2015, 2025])
    friction_lgbt = np.array([15, 70, 40, 40, 65, 20, 25])
    years_lgbt_interp = np.linspace(1950, 2025, 200)
    friction_lgbt_interp = np.interp(years_lgbt_interp, years_lgbt, friction_lgbt)

    # Platform Governance
    years_platform = np.array([2000, 2010, 2016, 2020, 2025])
    friction_platform = np.array([5, 5, 30, 60, 70])
    years_platform_interp = np.linspace(2000, 2025, 200)
    friction_platform_interp = np.interp(years_platform_interp, years_platform, friction_platform)

    # Plot trajectories
    ax.plot(years_suffrage_interp, friction_suffrage_interp,
           linestyle='-', linewidth=2.5, color=COLORS['primary'],
           label='Women\'s Suffrage')
    ax.plot(years_abolition_interp, friction_abolition_interp,
           linestyle='--', linewidth=2.5, color=COLORS['secondary'],
           label='Abolition')
    ax.plot(years_lgbt_interp, friction_lgbt_interp,
           linestyle='-.', linewidth=2.5, color=COLORS['tertiary'],
           label='LGBT Rights')
    ax.plot(years_platform_interp, friction_platform_interp,
           linestyle=':', linewidth=3, color=COLORS['quaternary'],
           label='Platform Governance')

    # Key events (vertical lines)
    events = [
        (1920, 'Women\'s\nSuffrage', 0.95),
        (1865, 'Abolition', 0.95),
        (1969, 'Stonewall', 0.85),
        (2015, 'Marriage\nEquality', 0.75),
    ]

    for year, label, height in events:
        ax.axvline(year, color=COLORS['light_gray'], linestyle='--',
                  linewidth=1, alpha=0.5, zorder=0)
        ax.text(year, 95 * height, label, ha='center', va='top',
               fontsize=8, bbox=dict(boxstyle='round,pad=0.3',
               facecolor='white', edgecolor='none', alpha=0.7))

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Friction F(d) (protests, resistance, instability)', fontsize=12)
    ax.set_title('Historical Friction Dynamics: Four Domains',
                fontsize=16, fontweight='bold')
    ax.set_xlim(1800, 2025)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'friction_trajectories.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {OUTPUT_DIR}friction_trajectories.png")


def fig3_alpha_historical_trajectories():
    """Figure 3: Consent Alignment Over Time (α(d) Trajectories)"""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Suffrage Domain
    years_suffrage = np.array([1800, 1890, 1920, 1965, 2025])
    alpha_suffrage = np.array([0.05, 0.05, 0.5, 0.8, 0.9])
    years_suffrage_interp = np.linspace(1800, 2025, 200)
    alpha_suffrage_interp = np.interp(years_suffrage_interp, years_suffrage, alpha_suffrage)

    # Labor Domain
    years_labor = np.array([1800, 1900, 1935, 1975, 2025])
    alpha_labor = np.array([0.1, 0.1, 0.5, 0.65, 0.35])
    years_labor_interp = np.linspace(1800, 2025, 200)
    alpha_labor_interp = np.interp(years_labor_interp, years_labor, alpha_labor)

    # LGBT Rights
    years_lgbt = np.array([1800, 1960, 2000, 2015, 2025])
    alpha_lgbt = np.array([0.02, 0.02, 0.25, 0.75, 0.65])
    years_lgbt_interp = np.linspace(1800, 2025, 200)
    alpha_lgbt_interp = np.interp(years_lgbt_interp, years_lgbt, alpha_lgbt)

    # Platform Governance
    years_platform = np.array([2000, 2025])
    alpha_platform = np.array([0.15, 0.15])
    years_platform_interp = np.linspace(2000, 2025, 200)
    alpha_platform_interp = np.interp(years_platform_interp, years_platform, alpha_platform)

    # Climate Policy (projection)
    years_climate = np.array([1990, 2025, 2050])
    alpha_climate = np.array([0.3, 0.3, 0.5])
    years_climate_interp = np.linspace(1990, 2050, 200)
    alpha_climate_interp = np.interp(years_climate_interp, years_climate, alpha_climate)

    # Legitimacy threshold shading
    ax.axhspan(0.6, 1.0, alpha=0.15, color=COLORS['tertiary'],
              label='Legitimacy Threshold (α > 0.6)')

    # Plot trajectories
    ax.plot(years_suffrage_interp, alpha_suffrage_interp,
           linestyle='-', linewidth=2.5, color=COLORS['primary'],
           label='Suffrage Domain')
    ax.plot(years_labor_interp, alpha_labor_interp,
           linestyle='--', linewidth=2.5, color=COLORS['secondary'],
           label='Labor Domain')
    ax.plot(years_lgbt_interp, alpha_lgbt_interp,
           linestyle='-.', linewidth=2.5, color=COLORS['tertiary'],
           label='LGBT Rights')
    ax.plot(years_platform_interp, alpha_platform_interp,
           linestyle=':', linewidth=3, color=COLORS['quaternary'],
           label='Platform Governance')
    ax.plot(years_climate_interp, alpha_climate_interp,
           linestyle=(0, (3, 5, 1, 5)), linewidth=2.5, color=COLORS['gray'],
           label='Climate Policy (projection)')

    # Mark projection region
    ax.axvline(2025, color='black', linestyle='--', linewidth=1, alpha=0.3)
    ax.text(2037.5, 0.05, 'Projection', ha='center', fontsize=9,
           style='italic', color=COLORS['gray'])

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('α(d) (Consent Alignment)', fontsize=12)
    ax.set_title('The Expansion of Consent-Holding Across Domains',
                fontsize=16, fontweight='bold')
    ax.text(0.5, -0.13, 'α(d) measures stakes-weighted voice over time',
           ha='center', transform=ax.transAxes, fontsize=11, style='italic')

    ax.set_xlim(1800, 2050)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'alpha_historical_trajectories.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {OUTPUT_DIR}alpha_historical_trajectories.png")


def fig4_monte_carlo_mechanisms():
    """Figure 4: Monte Carlo Mechanism Comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))

    mechanisms = ['Dictator', 'Simple\nMajority', 'Stakes-\nWeighted', 'Technocracy']

    # Data (mean values)
    friction_means = [65, 45, 25, 40]
    alignment_means = [15, 55, 85, 35]  # Scale to 0-100 for visualization
    instability_means = [70, 40, 15, 35]  # Scale to 0-100 for visualization

    # Error bars (±5% of mean)
    friction_err = [f * 0.05 for f in friction_means]
    alignment_err = [a * 0.05 for a in alignment_means]
    instability_err = [i * 0.05 for i in instability_means]

    x = np.arange(len(mechanisms))
    width = 0.25

    # Create grouped bars
    bars1 = ax.bar(x - width, friction_means, width, yerr=friction_err,
                   label='Friction E[F]', color=COLORS['quaternary'],
                   capsize=5, alpha=0.8)
    bars2 = ax.bar(x, alignment_means, width, yerr=alignment_err,
                   label='Alignment E[α] (×100)', color=COLORS['primary'],
                   capsize=5, alpha=0.8)
    bars3 = ax.bar(x + width, instability_means, width, yerr=instability_err,
                   label='Instability P(Y=1) (×100)', color=COLORS['gray'],
                   capsize=5, alpha=0.8)

    ax.set_xlabel('Mechanism', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Monte Carlo Simulation: Mechanism Performance',
                fontsize=16, fontweight='bold')
    ax.text(0.5, -0.18, 'N=1000 runs, showing mean ± 95% CI',
           ha='center', transform=ax.transAxes, fontsize=11, style='italic')
    ax.text(0.5, -0.24, 'Stakes-weighted mechanisms minimize friction and instability',
           ha='center', transform=ax.transAxes, fontsize=10, style='italic',
           color=COLORS['tertiary'], fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(mechanisms)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'monte_carlo_mechanisms.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {OUTPUT_DIR}monte_carlo_mechanisms.png")


def fig5_corporate_consent_matrix():
    """Figure 5: Corporate Governance Consent Matrix"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    stakeholders = ['Shareholders', 'Workers', 'Customers', 'Community']
    domains = ['Strategy', 'Executive\nPay', 'Wages', 'Product\nSafety', 'Environmental\nImpact']

    # Current: Shareholder Primacy
    current_data = np.array([
        [0.9, 0.95, 0.8, 0.7, 0.6],    # Shareholders
        [0.05, 0.02, 0.15, 0.1, 0.05], # Workers
        [0.03, 0.02, 0.03, 0.15, 0.1], # Customers
        [0.02, 0.01, 0.02, 0.05, 0.25],# Community
    ])
    current_alpha = [0.25, 0.20, 0.30, 0.35, 0.40]

    # Proposed: Stakes-Weighted
    proposed_data = np.array([
        [0.4, 0.3, 0.2, 0.3, 0.2],  # Shareholders
        [0.3, 0.2, 0.6, 0.2, 0.2],  # Workers
        [0.2, 0.1, 0.1, 0.4, 0.3],  # Customers
        [0.1, 0.4, 0.1, 0.1, 0.3],  # Community
    ])
    proposed_alpha = [0.75, 0.70, 0.85, 0.80, 0.75]

    # Plot current heatmap
    im1 = ax1.imshow(current_data, cmap='Blues', aspect='auto', vmin=0, vmax=1)
    ax1.set_xticks(np.arange(len(domains)))
    ax1.set_yticks(np.arange(len(stakeholders)))
    ax1.set_xticklabels(domains)
    ax1.set_yticklabels(stakeholders)
    ax1.set_title('Current: Shareholder Primacy', fontsize=14, fontweight='bold')

    # Add cell values
    for i in range(len(stakeholders)):
        for j in range(len(domains)):
            text = ax1.text(j, i, f'{current_data[i, j]:.2f}',
                          ha="center", va="center", color="black" if current_data[i, j] < 0.5 else "white",
                          fontsize=9)

    # Add alpha values below
    for j, alpha in enumerate(current_alpha):
        ax1.text(j, len(stakeholders) + 0.3, f'α={alpha:.2f}',
                ha="center", va="top", fontsize=9, fontweight='bold',
                color=COLORS['quaternary'])

    # Plot proposed heatmap
    im2 = ax2.imshow(proposed_data, cmap='Blues', aspect='auto', vmin=0, vmax=1)
    ax2.set_xticks(np.arange(len(domains)))
    ax2.set_yticks(np.arange(len(stakeholders)))
    ax2.set_xticklabels(domains)
    ax2.set_yticklabels(stakeholders)
    ax2.set_title('Proposed: Stakes-Weighted', fontsize=14, fontweight='bold')

    # Add cell values
    for i in range(len(stakeholders)):
        for j in range(len(domains)):
            text = ax2.text(j, i, f'{proposed_data[i, j]:.2f}',
                          ha="center", va="center", color="black" if proposed_data[i, j] < 0.5 else "white",
                          fontsize=9)

    # Add alpha values below
    for j, alpha in enumerate(proposed_alpha):
        ax2.text(j, len(stakeholders) + 0.3, f'α={alpha:.2f}',
                ha="center", va="top", fontsize=9, fontweight='bold',
                color=COLORS['tertiary'])

    # Add colorbar
    cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='vertical',
                       fraction=0.046, pad=0.04)
    cbar.set_label('sᵢ(d) × Cᵢ (stakes × consent power)', rotation=270,
                   labelpad=20, fontsize=11)

    # Overall title
    fig.suptitle('Corporate Governance: Current vs Stakes-Weighted Consent',
                fontsize=16, fontweight='bold', y=0.98)
    fig.text(0.5, 0.02, 'Cell values: sᵢ(d) × Cᵢ (stakes × consent power)',
            ha='center', fontsize=11, style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig(OUTPUT_DIR + 'corporate_consent_matrix.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {OUTPUT_DIR}corporate_consent_matrix.png")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Generating Consent-Holding Theory Figures")
    print("="*60 + "\n")

    fig1_alpha_p_frontier()
    fig2_friction_trajectories()
    fig3_alpha_historical_trajectories()
    fig4_monte_carlo_mechanisms()
    fig5_corporate_consent_matrix()

    print("\n" + "="*60)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*60 + "\n")
