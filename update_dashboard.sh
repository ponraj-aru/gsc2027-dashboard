#!/bin/zsh
# One-command refresh: uses the newest adminPapersBrowse_*.doc in this folder.
set -e
cd "$(dirname "$0")"
P=.venv/bin/python
SRC=$($P -c 'from source_config import SOURCE_DOC; print(SOURCE_DOC)')
echo "Source: $SRC"
for s in analyze_dataset build_word_clusters export_tables generate_maps prepare_dashboard_data \
         prepare_advanced_dashboard_data generate_visuals build_full_deck \
         build_poster_graphics build_marketing_poster build_linkedin_posters \
         build_poster_html build_wgs_reactive_dashboard; do
  echo "== $s"; $P $s.py | tail -1
done

cp gsc2027_interactive_world_map.html index.html
mkdir -p docs && cp gsc2027_interactive_world_map.html docs/index.html
mkdir -p docs/visuals && cp visuals/*.png docs/visuals/ 2>/dev/null || true
touch .nojekyll docs/.nojekyll
echo "Done. Shareable files updated: index.html & docs/index.html"

# Publish to GitHub Pages from repository root
git add index.html docs/ gsc2027_interactive_world_map.html visuals/ *.json *.csv *.xlsx *.pptx *.py .nojekyll 2>/dev/null || true
git commit -qm "Update dashboard with latest abstracts from $SRC as of $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
if git remote get-url origin >/dev/null 2>&1; then
  git push origin main && echo "Published to GitHub Pages (https://ponraj-aru.github.io/gsc2027-dashboard/)"
else
  echo "No GitHub remote set yet; skipping publish"
fi
