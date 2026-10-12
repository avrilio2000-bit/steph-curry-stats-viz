import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# set up file paths
base_dir = r"C:\Users\Lenovo\Downloads\archive"  
csv_path = os.path.join(base_dir, "Stephen Curry Postseason Stats.csv")
logos_dir = os.path.join(base_dir, "NBA_team_logos")

# map team codes to exact gif filenames in the folder
nba_teams = {
    'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets', 
    'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 
    'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons', 
    'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers', 
    'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 
    'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 
    'NOP': 'New Orleans Pelicans', 'NOH': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 
    'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 
    'PHX': 'Phoenix Suns', 'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 
    'SAS': 'San Antonio Spurs', 'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 
    'WAS': 'Washington Wizards'
}

# read the postseason dataset
df = pd.read_csv(csv_path)

# clean team column and map to full names
df['OPP'] = df['OPP'].astype(str).str.replace('@', '', regex=False).str.replace('vs', '', regex=False).str.strip()
df['Full_Name'] = df['OPP'].map(nba_teams).fillna(df['OPP'])

# convert points column to numeric numbers
df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')
df_clean = df.dropna(subset=['PTS'])

# calculate average ppg per playoff opponent
playoff_stats = df_clean.groupby('Full_Name').agg(
    Games_Played=('PTS', 'count'),
    Curry_PPG=('PTS', 'mean')
).reset_index()

# keep teams he faced at least 4 times in a series
playoff_stats = playoff_stats[playoff_stats['Games_Played'] >= 4]

# sort by highest ppg and take top 10
top_10 = playoff_stats.sort_values(by='Curry_PPG', ascending=False).head(10).reset_index(drop=True)

# create graph figure
fig, ax = plt.subplots(figsize=(12, 7))

# plot blue bars with yellow outline
bars = ax.bar(top_10['Full_Name'], top_10['Curry_PPG'], color='#1D428A', edgecolor='#FFC72C', linewidth=2, width=0.55)

# remove text labels from bottom axis so only gif logos show
ax.set_xticklabels([])

# add exact ppg values above each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0, 
        yval + 0.4, 
        f"{yval:.1f}", 
        ha='center', 
        va='bottom', 
        fontweight='bold', 
        fontsize=11
    )

# place image logos along x-axis
for i, row in top_10.iterrows():
    team = row['Full_Name']
    logo_file = os.path.join(logos_dir, f"{team}.gif")
    
    if os.path.exists(logo_file):
        # convert image to rgba so transparency works properly
        img = Image.open(logo_file).convert("RGBA")
        imagebox = OffsetImage(img, zoom=0.45)
        
        ab = AnnotationBbox(
            imagebox, 
            (i, 0), 
            xybox=(0, -25), 
            xycoords=('data', 'data'), 
            boxcoords="offset points", 
            frameon=False
        )
        ax.add_artist(ab)

# use single title block to stop font layering bugs
ax.set_title(
    "Stephen Curry: Highest Scoring Averages in the NBA Playoffs (2013–2023)\n"
    "Postseason Career Stats | Min. 4 Games Played", 
    fontsize=13, 
    fontweight='bold', 
    pad=15
)

ax.set_ylabel("Points Per Game (PPG)", fontsize=11, fontweight='bold')
ax.set_ylim(0, top_10['Curry_PPG'].max() + 5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# leave space at bottom so logos fit
fig.subplots_adjust(bottom=0.15)

# high-res PNG
plt.savefig("steph_curry_playoffs.png", dpi=300, bbox_inches='tight')
plt.show()
