from source_config import SOURCE_DOC
import json

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

countries_json = json.dumps(data['countries'], ensure_ascii=False)
themes_json = json.dumps(data['themes'], ensure_ascii=False)
regional_json = json.dumps(data['regional'], ensure_ascii=False)
word_clusters_json = json.dumps(data['word_clusters'], ensure_ascii=False)

# Read HTML template from a clean text file or string without f-string variable collisions
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GSC 2027 - Abstract Submissions & Thematic Landscape Dashboard</title>
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <!-- Google Fonts: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #FFFFFF;
            color: #1E293B;
            line-height: 1.5;
            padding: 24px 32px 48px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Top Navigation / Brand Header */
        header.dashboard-header {
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 20px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
            gap: 16px;
        }
        .header-titles h1 {
            font-size: 24px;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
        }
        .header-titles p {
            font-size: 14px;
            color: #64748B;
            margin-top: 4px;
        }
        .header-meta {
            font-size: 13px;
            color: #475569;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: 500;
        }

        /* KPI Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 14px;
            margin-bottom: 24px;
        }
        @media (max-width: 1100px) {
            .kpi-grid { grid-template-columns: repeat(3, 1fr); }
        }
        @media (max-width: 640px) {
            .kpi-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .kpi-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .kpi-card:hover, .kpi-card.active {
            border-color: #2563EB;
            background-color: #F8FAFC;
        }
        .kpi-card.active {
            border-left: 4px solid #2563EB;
        }
        .kpi-label {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #64748B;
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.1;
        }
        .kpi-sub {
            font-size: 11.5px;
            color: #475569;
            margin-top: 4px;
        }

        /* Section Headings */
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-subtitle {
            font-size: 13px;
            color: #64748B;
        }

        /* Filter Controls */
        .theme-selector-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 6px;
            margin-bottom: 18px;
        }
        .filter-btn {
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 7px 14px;
            font-size: 12.5px;
            font-weight: 500;
            color: #334155;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .filter-btn:hover {
            background: #F1F5F9;
            color: #0F172A;
            border-color: #94A3B8;
        }
        .filter-btn.active {
            background: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
            font-weight: 600;
        }

        /* Map Card */
        .map-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 28px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        #mapPlot {
            width: 100%;
            height: 560px;
        }
        .map-legend-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 18px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #F1F5F9;
            flex-wrap: wrap;
            font-size: 12px;
            color: #475569;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .legend-swatch {
            width: 16px;
            height: 12px;
            border-radius: 2px;
            border: 1px solid rgba(0,0,0,0.1);
        }

        /* Two Column Charts Grid */
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 28px;
        }
        @media (max-width: 900px) {
            .charts-grid { grid-template-columns: 1fr; }
        }
        .chart-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .chart-card h3 {
            font-size: 14px;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 8px;
        }

        /* Word Clusters Section */
        .cluster-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 28px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .word-cloud-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 16px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            margin-bottom: 18px;
            min-height: 150px;
            align-items: center;
            justify-content: center;
        }
        .word-badge {
            display: inline-flex;
            align-items: baseline;
            gap: 4px;
            padding: 4px 10px;
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            color: #1E293B;
            transition: all 0.15s ease;
            cursor: default;
        }
        .word-badge:hover {
            background: #EFF6FF;
            border-color: #2563EB;
            color: #1D4ED8;
        }
        .word-badge span.count {
            font-size: 11px;
            color: #64748B;
            font-weight: 600;
        }
        .cluster-details-grid {
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 18px;
        }
        @media (max-width: 850px) {
            .cluster-details-grid { grid-template-columns: 1fr; }
        }
        .subtopics-box {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 14px;
        }
        .subtopics-box h4 {
            font-size: 13px;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 10px;
        }
        .keyword-list {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .kw-tag {
            font-size: 12px;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 4px 8px;
            border-radius: 4px;
            color: #334155;
        }

        /* Table Card & Sorting */
        .table-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            margin-bottom: 30px;
        }
        .table-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .search-box {
            padding: 7px 12px;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            font-size: 13px;
            width: 280px;
            color: #1E293B;
            outline: none;
        }
        .search-box:focus {
            border-color: #2563EB;
        }
        .table-wrapper {
            overflow-x: auto;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
        }
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }
        table.data-table th {
            background-color: #F8FAFC;
            color: #334155;
            font-weight: 600;
            padding: 10px 12px;
            border-bottom: 1px solid #CBD5E1;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }
        table.data-table th:hover {
            background-color: #F1F5F9;
            color: #0F172A;
        }
        table.data-table th .sort-icon {
            display: inline-block;
            margin-left: 4px;
            font-size: 10px;
            color: #94A3B8;
        }
        table.data-table th.sorted .sort-icon {
            color: #2563EB;
        }
        table.data-table td {
            padding: 9px 12px;
            border-bottom: 1px solid #F1F5F9;
            color: #334155;
            white-space: nowrap;
        }
        table.data-table tr:hover td {
            background-color: #F8FAFC;
        }
        table.data-table td.num {
            text-align: right;
            font-variant-numeric: tabular-nums;
        }
        table.data-table th.num {
            text-align: right;
        }
        table.data-table td.total-col {
            font-weight: 600;
            color: #0F172A;
        }
        .theme-col-header {
            border-left: 1px solid #E2E8F0;
        }
        td.theme-cell {
            border-left: 1px solid #F1F5F9;
        }
        .table-footer-info {
            font-size: 12px;
            color: #64748B;
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Simple Footer */
        footer.dashboard-footer {
            border-top: 1px solid #E2E8F0;
            padding-top: 16px;
            font-size: 12px;
            color: #94A3B8;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <header class="dashboard-header">
        <div class="header-titles">
            <h1>Groningen Sustainability Conference 2027 (GSC 2027)</h1>
            <p>Abstract Submissions, Global Geographic Distribution & Thematic Analysis</p>
        </div>
        <div class="header-meta">
            Official Committee Dataset • 301 Submissions • 66 Primary Nations
        </div>
    </header>

    <!-- Top KPI Cards: Strictly Ordered -->
    <div class="kpi-grid">
        <div class="kpi-card active" onclick="selectThemeFilter(0)">
            <div class="kpi-label">All Submissions</div>
            <div class="kpi-value">301</div>
            <div class="kpi-sub">66 Nations • 100%</div>
        </div>
        <div class="kpi-card" onclick="selectThemeFilter(1)">
            <div class="kpi-label">Theme 1: SDGs Post-2030</div>
            <div class="kpi-value">60</div>
            <div class="kpi-sub">19.9% • 20 Nations</div>
        </div>
        <div class="kpi-card" onclick="selectThemeFilter(2)">
            <div class="kpi-label">Theme 2: Resilience</div>
            <div class="kpi-value">76</div>
            <div class="kpi-sub">25.2% • Largest Track</div>
        </div>
        <div class="kpi-card" onclick="selectThemeFilter(3)">
            <div class="kpi-label">Theme 3: Climate Nexus</div>
            <div class="kpi-value">75</div>
            <div class="kpi-sub">24.9% • 28 Nations</div>
        </div>
        <div class="kpi-card" onclick="selectThemeFilter(4)">
            <div class="kpi-label">Theme 4: Health & Society</div>
            <div class="kpi-value">45</div>
            <div class="kpi-sub">15.0% • 18 Nations</div>
        </div>
        <div class="kpi-card" onclick="selectThemeFilter(5)">
            <div class="kpi-label">Theme 5: AI & Digital</div>
            <div class="kpi-value">45</div>
            <div class="kpi-sub">15.0% • 19 Nations</div>
        </div>
    </div>

    <!-- Thematic Filter Buttons (Strict 1 -> 5 Order) -->
    <div class="section-header">
        <div>
            <div class="section-title">Geographic Distribution Map</div>
            <div class="section-subtitle">Click below to filter the global map, charts, and word clusters by theme</div>
        </div>
    </div>
    
    <div class="theme-selector-bar">
        <button class="filter-btn active" id="btn-theme-0" onclick="selectThemeFilter(0)">All Themes (301)</button>
        <button class="filter-btn" id="btn-theme-1" onclick="selectThemeFilter(1)">Theme 1: SDGs Beyond 2030 (60)</button>
        <button class="filter-btn" id="btn-theme-2" onclick="selectThemeFilter(2)">Theme 2: Resilience Across Systems (76)</button>
        <button class="filter-btn" id="btn-theme-3" onclick="selectThemeFilter(3)">Theme 3: Climate Change–Development Nexus (75)</button>
        <button class="filter-btn" id="btn-theme-4" onclick="selectThemeFilter(4)">Theme 4: Health & Well-being (45)</button>
        <button class="filter-btn" id="btn-theme-5" onclick="selectThemeFilter(5)">Theme 5: AI & Digitalization (45)</button>
    </div>

    <!-- Map Card -->
    <div class="map-card">
        <div id="mapPlot"></div>
        <div class="map-legend-bar" id="mapDiscreteLegend">
            <!-- Populated dynamically with discrete tiers -->
        </div>
    </div>

    <!-- Charts Section: Thematic Breakdown Pie Chart & Regional Chart -->
    <div class="section-header">
        <div>
            <div class="section-title">Program Analytics & Thematic Proportions</div>
            <div class="section-subtitle">Comparative shares across the 5 core themes and geographic regions</div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-card">
            <h3>Submissions by Theme (Percentage & Count)</h3>
            <div id="themePiePlot" style="height: 300px;"></div>
        </div>
        <div class="chart-card">
            <h3>Submissions by Continental Region</h3>
            <div id="regionBarPlot" style="height: 300px;"></div>
        </div>
    </div>

    <!-- Word Clusters Section -->
    <div class="section-header">
        <div>
            <div class="section-title">Abstract Word Clusters & Lexical Frequency</div>
            <div class="section-subtitle">Top terms and author keywords extracted directly from abstract text</div>
        </div>
    </div>

    <div class="cluster-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
            <div style="font-size: 14px; font-weight: 600; color: #0F172A;" id="clusterThemeTitle">
                Word Frequency Cluster — All Themes (301 Abstracts)
            </div>
            <div style="font-size: 12px; color: #64748B;">
                Filter words: <input type="text" id="wordFilterInput" placeholder="Search term..." onkeyup="filterWordBadges()" style="padding: 4px 8px; border: 1px solid #CBD5E1; border-radius: 4px; font-size: 12px;">
            </div>
        </div>

        <!-- Word Tags Cloud -->
        <div class="word-cloud-container" id="wordCloudBox">
            <!-- Injected by JavaScript -->
        </div>

        <!-- Two Column Details: Word Frequency Bar Chart & Author Keywords -->
        <div class="cluster-details-grid">
            <div class="subtopics-box">
                <h4>Top 12 Most Frequent Abstract Words</h4>
                <div id="wordBarPlot" style="height: 240px;"></div>
            </div>
            <div class="subtopics-box">
                <h4>Top Author-Supplied Keywords</h4>
                <div class="keyword-list" id="authorKeywordsList">
                    <!-- Injected by JavaScript -->
                </div>
            </div>
        </div>
    </div>

    <!-- Sortable Country Table -->
    <div class="section-header">
        <div>
            <div class="section-title">Participating Countries Leaderboard</div>
            <div class="section-subtitle">Click any column header to sort highest-to-lowest or lowest-to-highest</div>
        </div>
    </div>

    <div class="table-card">
        <div class="table-controls">
            <input type="text" id="countrySearch" class="search-box" placeholder="Search country or region..." onkeyup="renderTable()">
            <div style="font-size: 12.5px; color: #64748B;">
                Showing <span id="visibleRowCount" style="font-weight: 600; color: #0F172A;">66</span> countries • Click header to reverse sort
            </div>
        </div>

        <div class="table-wrapper">
            <table class="data-table" id="countriesTable">
                <thead>
                    <tr>
                        <th onclick="sortTable('rank')" id="th-rank">Rank <span class="sort-icon">▼</span></th>
                        <th onclick="sortTable('country')" id="th-country">Country <span class="sort-icon"></span></th>
                        <th onclick="sortTable('region')" id="th-region">Region <span class="sort-icon"></span></th>
                        <th onclick="sortTable('total')" id="th-total" class="num sorted">Total Papers <span class="sort-icon">▼</span></th>
                        <th onclick="sortTable('t1')" id="th-t1" class="num theme-col-header">Theme 1 <span class="sort-icon"></span></th>
                        <th onclick="sortTable('t2')" id="th-t2" class="num theme-col-header">Theme 2 <span class="sort-icon"></span></th>
                        <th onclick="sortTable('t3')" id="th-t3" class="num theme-col-header">Theme 3 <span class="sort-icon"></span></th>
                        <th onclick="sortTable('t4')" id="th-t4" class="num theme-col-header">Theme 4 <span class="sort-icon"></span></th>
                        <th onclick="sortTable('t5')" id="th-t5" class="num theme-col-header">Theme 5 <span class="sort-icon"></span></th>
                        <th onclick="sortTable('oral')" id="th-oral" class="num">Oral <span class="sort-icon"></span></th>
                        <th onclick="sortTable('poster')" id="th-poster" class="num">Poster <span class="sort-icon"></span></th>
                        <th onclick="sortTable('special')" id="th-special" class="num">Panels <span class="sort-icon"></span></th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <!-- Populated by JavaScript -->
                </tbody>
            </table>
        </div>
        <div class="table-footer-info">
            <span>Note: Theme columns are arranged in strict sequential order (Theme 1 through Theme 5).</span>
            <span>Total Submissions: 301</span>
        </div>
    </div>

    <!-- Footer -->
    <footer class="dashboard-footer">
        Groningen Sustainability Conference 2027 (GSC 2027) • University of Groningen, Netherlands • Data Source: ConfTool Submissions Dataset
    </footer>
</div>

<script>
// Raw data injected from python
const countryData = """ + countries_json + """;
const themesSummary = """ + themes_json + """;
const regionalSummary = """ + regional_json + """;
const wordClusters = """ + word_clusters_json + """;

let currentTheme = 0; // 0 = All, 1 = T1, 2 = T2, 3 = T3, 4 = T4, 5 = T5
let sortColumn = 'total';
let sortDirection = 'desc'; // 'asc' or 'desc'

// Discrete Color Palettes for the Map
const DISCRETE_TIERS_ALL = [
    { label: "21+ papers", min: 21, max: 999, color: "#1E3A8A" },
    { label: "11 – 20 papers", min: 11, max: 20, color: "#2563EB" },
    { label: "6 – 10 papers", min: 6, max: 10, color: "#60A5FA" },
    { label: "3 – 5 papers", min: 3, max: 5, color: "#93C5FD" },
    { label: "1 – 2 papers", min: 1, max: 2, color: "#DBEAFE" }
];

const DISCRETE_TIERS_THEME = [
    { label: "6+ papers", min: 6, max: 999, color: "#1E3A8A" },
    { label: "4 – 5 papers", min: 4, max: 5, color: "#2563EB" },
    { label: "2 – 3 papers", min: 2, max: 3, color: "#60A5FA" },
    { label: "1 paper", min: 1, max: 1, color: "#BFDBFE" }
];

// Initialize on Load
document.addEventListener("DOMContentLoaded", function() {
    renderMap();
    renderThemePieChart();
    renderRegionBarChart();
    updateWordClusterSection();
    renderTable();
});

// ----------------------------------------------------------------------------
// 1. Theme Filter Handler
// ----------------------------------------------------------------------------
function selectThemeFilter(tNum) {
    currentTheme = tNum;
    
    // Update Filter Buttons
    for (let i = 0; i <= 5; i++) {
        const btn = document.getElementById("btn-theme-" + i);
        if (btn) {
            if (i === tNum) btn.classList.add('active');
            else btn.classList.remove('active');
        }
    }
    
    // Update KPI Card active borders
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach((c, idx) => {
        if (idx === tNum) c.classList.add('active');
        else c.classList.remove('active');
    });

    renderMap();
    updateWordClusterSection();
    
    // If a theme is selected, auto-sort table by that theme column descending
    if (tNum > 0) {
        sortColumn = "t" + tNum;
        sortDirection = 'desc';
    } else {
        sortColumn = 'total';
        sortDirection = 'desc';
    }
    renderTable();
}

// ----------------------------------------------------------------------------
// 2. Interactive Map with Discrete Tiers
// ----------------------------------------------------------------------------
function renderMap() {
    const tiers = (currentTheme === 0) ? DISCRETE_TIERS_ALL : DISCRETE_TIERS_THEME;
    const valueKey = (currentTheme === 0) ? 'total' : ("t" + currentTheme);
    
    // Group countries into discrete tiers
    const traces = [];
    
    // Render from lowest tier to highest tier
    tiers.slice().reverse().forEach(tier => {
        const matchingCountries = countryData.filter(c => c[valueKey] >= tier.min && c[valueKey] <= tier.max);
        
        const locs = matchingCountries.map(c => c.country);
        const zVals = matchingCountries.map(c => c[valueKey]);
        const customdata = matchingCountries.map(c => [
            c.country, c.region, c[valueKey], c.total, c.oral, c.poster, c.special,
            c.t1, c.t2, c.t3, c.t4, c.t5
        ]);

        const themeName = (currentTheme === 0) ? "Total Submissions" : ("Theme " + currentTheme + " Submissions");

        traces.push({
            type: 'choropleth',
            locations: locs,
            locationmode: 'country names',
            z: zVals,
            name: tier.label,
            colorscale: [[0, tier.color], [1, tier.color]],
            showscale: false,
            marker: {
                line: { color: '#CBD5E1', width: 0.8 }
            },
            customdata: customdata,
            hovertemplate: 
                "<b>%{customdata[0]}</b> (%{customdata[1]})<br>" +
                "━━━━━━━━━━━━━━━━━━━━━━━<br>" +
                "<b>" + themeName + ": %{customdata[2]}</b><br>" +
                "Total Conference Papers: %{customdata[3]}<br>" +
                "Oral: %{customdata[4]} | Poster: %{customdata[5]} | Panels: %{customdata[6]}<br>" +
                "──────── All Themes ────────<br>" +
                "Theme 1: %{customdata[7]} | Theme 2: %{customdata[8]}<br>" +
                "Theme 3: %{customdata[9]} | Theme 4: %{customdata[10]}<br>" +
                "Theme 5: %{customdata[11]}<br>" +
                "<extra></extra>"
        });
    });

    const layout = {
        title: false,
        geo: {
            showframe: false,
            showcoastlines: true,
            coastlinecolor: '#CBD5E1',
            showcountries: true,
            countrycolor: '#E2E8F0',
            landcolor: '#F8FAFC',
            lakecolor: '#FFFFFF',
            bgcolor: '#FFFFFF',
            projection: { type: 'natural earth' }
        },
        margin: { l: 0, r: 0, t: 10, b: 0 },
        paper_bgcolor: '#FFFFFF',
        showlegend: false
    };

    Plotly.newPlot('mapPlot', traces, layout, { responsive: true, displayModeBar: false });

    // Render Clean Discrete Legend HTML Below Map
    const legendBox = document.getElementById('mapDiscreteLegend');
    let legHtml = '<b>Discrete Submission Tiers:</b> ';
    tiers.forEach(t => {
        legHtml += '<div class="legend-item">' +
            '<span class="legend-swatch" style="background-color: ' + t.color + ';"></span>' +
            '<span>' + t.label + '</span>' +
        '</div>';
    });
    legHtml += '<div class="legend-item">' +
        '<span class="legend-swatch" style="background-color: #F8FAFC; border: 1px dashed #CBD5E1;"></span>' +
        '<span>No submissions (0)</span>' +
    '</div>';
    legendBox.innerHTML = legHtml;
}

// ----------------------------------------------------------------------------
// 3. Theme Distribution Pie / Donut Chart
// ----------------------------------------------------------------------------
function renderThemePieChart() {
    const labels = themesSummary.map(t => t.short);
    const values = themesSummary.map(t => t.count);
    
    // Academic discrete colors: Royal Blue, Slate Blue, Teal, Indigo, Sky Blue
    const colors = ['#2563EB', '#0D9488', '#4F46E5', '#0284C7', '#6366F1'];

    const data = [{
        type: 'pie',
        labels: labels,
        values: values,
        hole: 0.48,
        sort: false, // Maintain strict Theme 1 -> Theme 5 order!
        marker: { colors: colors, line: { color: '#FFFFFF', width: 2 } },
        textinfo: 'label+percent',
        textposition: 'inside',
        insidetextorientation: 'horizontal',
        insidetextfont: { color: '#FFFFFF', size: 11, weight: 600 },
        hovertemplate: "<b>%{label}</b><br>Submissions: %{value}<br>Proportion: %{percent}<extra></extra>"
    }];

    const layout = {
        showlegend: false,
        margin: { l: 20, r: 20, t: 20, b: 20 },
        paper_bgcolor: '#FFFFFF',
        font: { family: 'Inter, sans-serif' }
    };

    Plotly.newPlot('themePiePlot', data, layout, { responsive: true, displayModeBar: false });
}

// ----------------------------------------------------------------------------
// 4. Regional Distribution Bar Chart
// ----------------------------------------------------------------------------
function renderRegionBarChart() {
    const regions = regionalSummary.map(r => r.region);
    const counts = regionalSummary.map(r => r.count);
    const pcts = regionalSummary.map(r => r.pct);

    const data = [{
        type: 'bar',
        x: regions,
        y: counts,
        text: counts.map((c, i) => c + " (" + pcts[i] + "%)"),
        textposition: 'auto',
        textfont: { size: 11, weight: 600, color: '#0F172A' },
        marker: {
            color: '#3B82F6',
            line: { color: '#1D4ED8', width: 1 }
        },
        hovertemplate: "<b>%{x}</b><br>Submissions: %{y}<extra></extra>"
    }];

    const layout = {
        margin: { l: 40, r: 20, t: 20, b: 35 },
        paper_bgcolor: '#FFFFFF',
        plot_bgcolor: '#FFFFFF',
        yaxis: {
            gridcolor: '#F1F5F9',
            title: false,
            zeroline: false
        },
        xaxis: {
            gridcolor: 'transparent',
            tickfont: { size: 12, weight: 600, color: '#334155' }
        },
        font: { family: 'Inter, sans-serif' }
    };

    Plotly.newPlot('regionBarPlot', data, layout, { responsive: true, displayModeBar: false });
}

// ----------------------------------------------------------------------------
// 5. Word Clusters & Frequency Explorer
// ----------------------------------------------------------------------------
function updateWordClusterSection() {
    const clusterObj = wordClusters[String(currentTheme)];
    if (!clusterObj) return;

    // Title update
    const titleBox = document.getElementById('clusterThemeTitle');
    titleBox.innerText = "Word Frequency Cluster — " + clusterObj.theme_title + " (" + clusterObj.papers_count + " Abstracts, " + clusterObj.total_words + " analyzed words)";

    // Render Word Badges (Font size scaled to frequency)
    const box = document.getElementById('wordCloudBox');
    const words = clusterObj.top_words;
    const maxCount = words.length > 0 ? words[0].count : 1;
    const minCount = words.length > 0 ? words[words.length - 1].count : 1;

    let badgesHtml = '';
    words.forEach(w => {
        // Scale font size between 12px and 22px
        const ratio = (w.count - minCount) / Math.max(1, (maxCount - minCount));
        const fSize = 12 + Math.round(ratio * 10);
        const fWeight = ratio > 0.4 ? '600' : '500';
        const color = ratio > 0.5 ? '#1E40AF' : '#1E293B';
        
        badgesHtml += '<span class="word-badge" style="font-size: ' + fSize + 'px; font-weight: ' + fWeight + '; color: ' + color + ';">' +
            w.word + ' <span class="count">(' + w.count + ')</span>' +
        '</span>';
    });
    box.innerHTML = badgesHtml;

    // Render Top 12 Word Frequency Horizontal Bar Chart
    const top12 = words.slice(0, 12).reverse();
    const wData = [{
        type: 'bar',
        orientation: 'h',
        y: top12.map(x => x.word),
        x: top12.map(x => x.count),
        text: top12.map(x => "" + x.count),
        textposition: 'auto',
        textfont: { size: 11, weight: 600, color: '#0F172A' },
        marker: { color: '#60A5FA', line: { color: '#2563EB', width: 1 } },
        hovertemplate: "<b>%{y}</b>: %{x} mentions<extra></extra>"
    }];

    const wLayout = {
        margin: { l: 95, r: 25, t: 10, b: 25 },
        paper_bgcolor: '#F8FAFC',
        plot_bgcolor: '#F8FAFC',
        xaxis: { gridcolor: '#E2E8F0', title: false, zeroline: false },
        yaxis: { tickfont: { size: 11, weight: 600, color: '#334155' } },
        font: { family: 'Inter, sans-serif' }
    };

    Plotly.newPlot('wordBarPlot', wData, wLayout, { responsive: true, displayModeBar: false });

    // Render Author Keywords List
    const kwBox = document.getElementById('authorKeywordsList');
    let kwHtml = '';
    clusterObj.top_keywords.forEach(k => {
        kwHtml += '<span class="kw-tag"><b>' + k.keyword + '</b> (' + k.count + ')</span> ';
    });
    kwBox.innerHTML = kwHtml || '<span style="color:#94A3B8; font-size:12px;">No keywords listed</span>';
}

function filterWordBadges() {
    const query = document.getElementById('wordFilterInput').value.toLowerCase().trim();
    const badges = document.querySelectorAll('#wordCloudBox .word-badge');
    badges.forEach(b => {
        const txt = b.innerText.toLowerCase();
        if (!query || txt.includes(query)) {
            b.style.display = 'inline-flex';
        } else {
            b.style.display = 'none';
        }
    });
}

// ----------------------------------------------------------------------------
// 6. Sortable Interactive Table
// ----------------------------------------------------------------------------
function sortTable(column) {
    if (sortColumn === column) {
        // Toggle direction
        sortDirection = (sortDirection === 'asc') ? 'desc' : 'asc';
    } else {
        sortColumn = column;
        sortDirection = (column === 'country' || column === 'region') ? 'asc' : 'desc';
    }
    
    // Update headers UI
    const allTh = document.querySelectorAll('table.data-table th');
    allTh.forEach(th => {
        th.classList.remove('sorted');
        const icon = th.querySelector('.sort-icon');
        if (icon) icon.innerText = '';
    });

    const activeTh = document.getElementById("th-" + column);
    if (activeTh) {
        activeTh.classList.add('sorted');
        const icon = activeTh.querySelector('.sort-icon');
        if (icon) icon.innerText = (sortDirection === 'asc') ? '▲' : '▼';
    }

    renderTable();
}

function renderTable() {
    const query = document.getElementById('countrySearch').value.toLowerCase().trim();
    
    // Filter
    let filtered = countryData.filter(c => {
        if (!query) return true;
        return c.country.toLowerCase().includes(query) || c.region.toLowerCase().includes(query);
    });

    // Sort
    filtered.sort((a, b) => {
        let valA = a[sortColumn];
        let valB = b[sortColumn];

        if (typeof valA === 'string') {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
            if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
            if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        } else {
            return sortDirection === 'asc' ? (valA - valB) : (valB - valA);
        }
    });

    document.getElementById('visibleRowCount').innerText = filtered.length;

    const tbody = document.getElementById('tableBody');
    let html = '';

    filtered.forEach(row => {
        html += '<tr>' +
            '<td style="color:#64748B; font-weight:600;">#' + row.rank + '</td>' +
            '<td><b>' + row.country + '</b></td>' +
            '<td>' + row.region + '</td>' +
            '<td class="num total-col">' + row.total + '</td>' +
            '<td class="num theme-cell">' + (row.t1 || '-') + '</td>' +
            '<td class="num theme-cell">' + (row.t2 || '-') + '</td>' +
            '<td class="num theme-cell">' + (row.t3 || '-') + '</td>' +
            '<td class="num theme-cell">' + (row.t4 || '-') + '</td>' +
            '<td class="num theme-cell">' + (row.t5 || '-') + '</td>' +
            '<td class="num">' + row.oral + '</td>' +
            '<td class="num">' + row.poster + '</td>' +
            '<td class="num">' + row.special + '</td>' +
        '</tr>';
    });

    tbody.innerHTML = html;
}
</script>
</body>
</html>
"""

with open('gsc2027_interactive_world_map.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("gsc2027_interactive_world_map.html successfully regenerated without any syntax errors!")
