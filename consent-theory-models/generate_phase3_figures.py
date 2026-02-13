"""
Phase 3 Figure Generation: Historical Alpha Time Series
Generates fig:alpha-suffrage and fig:alpha-abolition for v2.0.0 monograph.

Data sourced from:
  - V-Dem v15 Country-Year Core (v2x_suffr) for suffrage figure
  - Table tab:abolition-trajectories (v2.0.0) for abolition figure
  - Supplementary text values (Emancipation Proclamation 1863 alpha~0.25)

Suffrage figure uses annual V-Dem data with institutional milestones annotated.
Abolition figure uses step functions from paper's ordinal scale (no V-Dem equivalent).

Output: PDF (primary) + PNG (backup) to ../figures/
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import os

# =============================================================================
# Publication quality settings — serif fonts for academic paper
# =============================================================================
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Computer Modern Roman'],
    'font.size': 10,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.color': '#cccccc',
    'grid.linestyle': '--',
    'mathtext.fontset': 'cm',
    'figure.constrained_layout.use': True,
})

# =============================================================================
# Color palette — distinct, colorblind-accessible
# =============================================================================
COLORS = {
    'uk':         '#1f77b4',   # Steel blue
    'us':         '#d62728',   # Crimson
    'france':     '#2ca02c',   # Forest green
    'switzerland':'#ff7f0e',   # Amber
    'nz':         '#9467bd',   # Plum
    'haiti':      '#e377c2',   # Orchid
    'british_empire': '#1f77b4',
    'burgundy':   '#8B0000',   # Paper accent color
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'figures')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')


def load_vdem_suffrage():
    """Load V-Dem v2x_suffr for target countries."""
    csv_path = os.path.join(DATA_DIR, 'vdem_consent_subset.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f'{csv_path} not found. Run the extraction step first '
            '(extract V-Dem-CY-Core-v15.csv and filter to target countries).'
        )
    df = pd.read_csv(csv_path)
    return df


def fig_alpha_suffrage():
    """
    fig:alpha-suffrage — V-Dem annual suffrage data for five nations.

    Plots v2x_suffr (share of population with suffrage, 0-1) from V-Dem v15.
    Key institutional moments from Table tab:suffrage-alpha annotated.
    """
    df = load_vdem_suffrage()
    fig, ax = plt.subplots(figsize=(9, 5))

    # Country config: (V-Dem code, display name, color, linestyle, linewidth)
    countries = [
        ('GBR', 'United Kingdom',  COLORS['uk'],          '-',              2.0),
        ('USA', 'United States',   COLORS['us'],          '--',             2.0),
        ('FRA', 'France',          COLORS['france'],      '-.',             2.0),
        ('CHE', 'Switzerland',     COLORS['switzerland'], (0, (5, 2)),      2.0),
        ('NZL', 'New Zealand',     COLORS['nz'],          (0, (3, 1, 1, 1)), 1.8),
    ]

    for code, name, color, ls, lw in countries:
        cdf = df[(df.country_text_id == code) & (df.year <= 1980)].sort_values('year')
        cdf = cdf.dropna(subset=['v2x_suffr'])
        ax.plot(cdf.year, cdf.v2x_suffr * 100, label=name,
                color=color, linestyle=ls, linewidth=lw)

    # Annotate key institutional moments
    annots = [
        (1928, 100, 'UK: Equal\nFranchise\n1928',       (-52, -32), 'right'),
        (1966, 100, 'US: Voting\nRights Act\n1965',     (6, -28),   'left'),
        (1893, 100, 'NZ: Universal\nSuffrage 1893',     (-8, 6),    'right'),
        (1945, 100, 'France:\nWomen 1944',              (6, -22),   'left'),
        (1972, 100, 'Switzerland:\nWomen 1971',          (6, 4),     'left'),
    ]
    for year, alpha, text, (dx, dy), ha in annots:
        ax.annotate(text, xy=(year, alpha), xytext=(dx, dy),
                    textcoords='offset points', fontsize=7, ha=ha,
                    arrowprops=dict(arrowstyle='->', color='#888888',
                                    lw=0.7, connectionstyle='arc3,rad=0.1'),
                    bbox=dict(boxstyle='round,pad=0.2', fc='white',
                              ec='#cccccc', alpha=0.85))

    ax.set_xlabel('Year')
    ax.set_ylabel(
        r'$\hat{\alpha}(d_{\mathrm{suffrage}}, t)$'
        r' — V-Dem suffrage share (\%)'
    )
    ax.set_xlim(1789, 1982)
    ax.set_ylim(0, 110)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_yticks([0, 20, 40, 60, 80, 100])

    ax.legend(loc='upper left', frameon=True, fancybox=False,
              edgecolor='#cccccc', framealpha=0.9)

    # Source note
    ax.text(0.99, 0.02, r'Source: V-Dem v15, v2x\_suffr',
            transform=ax.transAxes, fontsize=6.5, ha='right', va='bottom',
            color='#999999', style='italic')

    for fmt in ('pdf', 'png'):
        path = os.path.join(OUTPUT_DIR, f'alpha_suffrage.{fmt}')
        fig.savefig(path, bbox_inches='tight')
        print(f'  -> {path}')
    plt.close(fig)


def fig_alpha_abolition():
    """
    fig:alpha-abolition — Abolition ordinal alpha trajectories for four polities.

    Data from Table tab:abolition-trajectories plus text-specified
    Emancipation Proclamation (1863, alpha~0.25) from line 1207.
    Step function visualization — no V-Dem equivalent for this construct.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # (year, ordinal_alpha) — step function
    british = [
        (1760, 0.00),   # Chattel slavery baseline
        (1772, 0.05),   # Somerset ruling
        (1807, 0.10),   # Slave Trade Act
        (1833, 0.50),   # Slavery Abolition Act
        (1838, 0.75),   # Apprenticeship ends
    ]
    us = [
        (1760, 0.00),   # Chattel slavery baseline
        (1787, 0.05),   # Northwest Ordinance
        (1808, 0.10),   # International trade ban
        (1863, 0.25),   # Emancipation Proclamation (limited, war measure)
        (1865, 0.50),   # 13th Amendment
        (1870, 0.75),   # 14th & 15th Amendments
        (1965, 0.90),   # Civil Rights Act + Voting Rights Act
    ]
    haiti = [
        (1760, 0.00),   # Chattel slavery baseline
        (1804, 0.75),   # Revolution: independence
    ]
    france = [
        (1760, 0.00),   # Chattel slavery baseline
        (1794, 0.50),   # National Convention abolishes slavery
        (1802, 0.00),   # Napoleon restores slavery
        (1848, 0.75),   # Final abolition (Second Republic)
    ]

    polities = [
        ('British Empire', british, COLORS['british_empire'], '-',              2.0),
        ('United States',  us,      COLORS['us'],             '--',             2.0),
        ('Haiti',          haiti,   COLORS['haiti'],          '-.',             2.0),
        ('France',         france,  COLORS['france'],         (0, (5, 2)),      2.0),
    ]

    for name, data, color, ls, lw in polities:
        years = [d[0] for d in data]
        alphas = [d[1] for d in data]
        years.append(1975)
        alphas.append(alphas[-1])
        ax.step(years, alphas, where='post', label=name,
                color=color, linestyle=ls, linewidth=lw)
        ax.scatter([d[0] for d in data], [d[1] for d in data],
                   color=color, s=18, zorder=5, edgecolors='white', linewidths=0.3)

    # Civil War shading
    ax.axvspan(1861, 1865, alpha=0.06, color=COLORS['us'], zorder=0)
    ax.text(1863, -0.02, 'US Civil War', fontsize=6.5, ha='center',
            color=COLORS['us'], alpha=0.6, style='italic')

    # Annotations
    annots = [
        # French reversal
        (1802, 0.00, 'Napoleon restores\nslavery (1802)',
         (12, 12), 'left', '#fff3f3'),
        # Haitian revolution
        (1804, 0.75, 'Haitian Revolution\n(1791\u20131804)',
         (-8, 10), 'right', 'white'),
        # US Jim Crow gap
        (1918, 0.75, '95-year gap:\nformal \u2192 effective\ncitizenship',
         (-10, -35), 'right', 'white'),
        # British gradualism
        (1838, 0.75, 'Apprenticeship\nends (1838)',
         (8, 8), 'left', 'white'),
    ]
    for year, alpha, text, (dx, dy), ha, fc in annots:
        ax.annotate(text, xy=(year, alpha), xytext=(dx, dy),
                    textcoords='offset points', fontsize=7, ha=ha,
                    arrowprops=dict(arrowstyle='->', color='#888888',
                                    lw=0.7, connectionstyle='arc3,rad=0.1'),
                    bbox=dict(boxstyle='round,pad=0.2', fc=fc,
                              ec='#cccccc', alpha=0.85))

    ax.set_xlabel('Year')
    ax.set_ylabel(
        r'$\hat{\alpha}(d_{\mathrm{slavery}}, t)$'
        r' — ordinal legal status index'
    )
    ax.set_xlim(1755, 1975)
    ax.set_ylim(-0.08, 1.05)

    # Right-side ordinal scale labels
    ax2 = ax.twinx()
    ax2.set_ylim(-0.08, 1.05)
    ordinal_ticks = [0.00, 0.10, 0.25, 0.50, 0.75, 0.90]
    ordinal_labels = [
        'Chattel slavery',
        'Amelioration',
        'Gradual eman.',
        'Immed. eman.',
        'Legal citizenship',
        'Effective cit.',
    ]
    ax2.set_yticks(ordinal_ticks)
    ax2.set_yticklabels(ordinal_labels, fontsize=7)
    ax2.tick_params(axis='y', length=0, pad=4)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color('#dddddd')
    ax2.spines['top'].set_visible(False)

    ax.legend(loc='center left', frameon=True, fancybox=False,
              edgecolor='#cccccc', framealpha=0.9)

    for fmt in ('pdf', 'png'):
        path = os.path.join(OUTPUT_DIR, f'alpha_abolition.{fmt}')
        fig.savefig(path, bbox_inches='tight')
        print(f'  -> {path}')
    plt.close(fig)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f'Output directory: {OUTPUT_DIR}\n')

    print('Generating fig:alpha-suffrage (V-Dem v15 data)...')
    fig_alpha_suffrage()

    print('\nGenerating fig:alpha-abolition (ordinal table data)...')
    fig_alpha_abolition()

    print('\nPhase 3 figures complete.')
