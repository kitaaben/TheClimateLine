class ClimateImpact {
  constructor() {
    this.rules = this.buildRules();
  }

  buildRules() {
    return [
      {
        id: 'food-crop-failure',
        category: 'Food',
        severity: 'severe',
        trigger: t => t.currentYear.maxTemp >= APP.THRESHOLDS.TEMP_CRITICAL && t.consecutiveHotYears >= 2,
        statement: t => ({
          title: `Crop failure risk in ${t.city.name}`,
          body: `${t.consecutiveHotYears} consecutive years above ${APP.THRESHOLDS.TEMP_CRITICAL}°C. If this continues, local crop yields could drop 60%+ within ${3 - t.consecutiveHotYears + 1} years.`,
          year: new Date().getFullYear() + Math.max(2, t.consecutiveHotYears),
          confidence: t.hotDaysCounts.above43.length >= 3 ? 'high' : 'medium',
        }),
      },
      {
        id: 'heat-health',
        category: 'Health',
        severity: 'moderate',
        trigger: t => t.trends.avgMax.slope > 0 && t.currentYear.maxTemp >= APP.THRESHOLDS.TEMP_WARN && t.consecutiveHotYears >= 2,
        statement: t => ({
          title: `Heat stress rising in ${t.city.name}`,
          body: `Warming at ${t.warmingRatePerYear.toFixed(2)}°C/year. If this trend holds, heat-related illness cases will rise significantly within 3 years.`,
          year: new Date().getFullYear() + 3,
          confidence: t.trends.avgMax.rSquared > 0.7 ? 'high' : 'medium',
        }),
      },
      {
        id: 'uninhabitable',
        category: 'Habitability',
        severity: 'critical',
        trigger: t => t.currentYear.maxTemp >= APP.THRESHOLDS.TEMP_EXTREME && t.consecutiveHotYears >= 3,
        statement: t => ({
          title: `${t.city.name} may become partially uninhabitable`,
          body: `${t.consecutiveHotYears} consecutive years exceeding ${APP.THRESHOLDS.TEMP_EXTREME}°C. At this rate, 4+ months of extreme heat annually by ${new Date().getFullYear() + 6}.`,
          year: new Date().getFullYear() + 6,
          confidence: t.trends.avgMax.rSquared > 0.6 ? 'medium' : 'low',
        }),
      },
      {
        id: 'infrastructure-strain',
        category: 'Infrastructure',
        severity: 'severe',
        trigger: t => t.currentYear.maxTemp >= APP.THRESHOLDS.TEMP_EXTREME && t.consecutiveHotYears >= 2,
        statement: t => ({
          title: `Infrastructure strain in ${t.city.name}`,
          body: `${t.consecutiveHotYears} years above ${APP.THRESHOLDS.TEMP_EXTREME}°C. Road buckling, rail warping, and power grid overloads become likely within 2 years.`,
          year: new Date().getFullYear() + 2,
          confidence: t.hotDaysCounts.above45.length >= 3 ? 'high' : 'medium',
        }),
      },
      {
        id: 'night-heat',
        category: 'Health',
        severity: 'severe',
        trigger: t => t.yearlyData.length >= 2 && t.yearlyData.slice(-3).some(d => d.minTemp >= APP.THRESHOLDS.NIGHT_DANGER),
        statement: t => ({
          title: `No overnight relief in ${t.city.name}`,
          body: `Nights above ${APP.THRESHOLDS.NIGHT_DANGER}°C mean no cooling off. Heat-related mortality could rise 15%+ in vulnerable populations within 4 years.`,
          year: new Date().getFullYear() + 4,
          confidence: 'medium',
        }),
      },
      {
        id: 'hot-days-accelerating',
        category: 'Health',
        severity: 'moderate',
        trigger: t => t.trends.hotDays35 && t.trends.hotDays35.slope > 3,
        statement: t => {
          const cur = t.hotDaysCounts.above35[t.hotDaysCounts.above35.length - 1] || 0;
          return {
            title: `Dangerous days accelerating in ${t.city.name}`,
            body: `Days above ${APP.THRESHOLDS.TEMP_WARN}°C increasing by ${t.trends.hotDays35.slope.toFixed(1)}/year. From ${cur} days to ${Math.round(cur + t.trends.hotDays35.slope * 4)} by ${new Date().getFullYear() + 4}.`,
            year: new Date().getFullYear() + 4,
            confidence: t.trends.hotDays35.rSquared > 0.7 ? 'high' : 'medium',
          };
        },
      },
      {
        id: 'compound-drought-heat',
        category: 'Food+Water',
        severity: 'critical',
        trigger: t => t.yearlyData.length >= 2 && t.yearlyData.slice(-2).every(d => d.maxTemp >= APP.THRESHOLDS.TEMP_CRITICAL && d.totalPrecip < 30),
        statement: t => ({
          title: `Compound drought-heat in ${t.city.name}`,
          body: `Two consecutive years of extreme heat + minimal rainfall. Crop failure and water shortages imminent within 2 years.`,
          year: new Date().getFullYear() + 2,
          confidence: 'high',
        }),
      },
      {
        id: 'warming-acceleration',
        category: 'Global',
        severity: 'severe',
        trigger: t => t.trends.avgMax && t.trends.avgMax.slope >= 0.05,
        statement: t => {
          const yr = new Date().getFullYear() + Math.round((2 - t.trends.avgMax.slope * 10) / t.trends.avgMax.slope);
          return {
            title: `Warming accelerating in ${t.city.name}`,
            body: `Rising at ${(t.trends.avgMax.slope * 10).toFixed(2)}°C/decade. Could exceed IPCC 2°C threshold by ${yr} if global trends align.`,
            year: yr,
            confidence: t.trends.avgMax.rSquared > 0.8 ? 'high' : 'medium',
          };
        },
      },
    ];
  }

  evaluate(trends) {
    if (!trends || trends.yearlyData.length < 2) return { statements: [], error: 'Need 2+ years' };
    const triggered = [];
    for (const rule of this.rules) {
      try { if (rule.trigger(trends)) triggered.push({ id: rule.id, category: rule.category, severity: rule.severity, ...rule.statement(trends) }); } catch { }
    }
    const order = { critical: 0, severe: 1, moderate: 2 };
    triggered.sort((a, b) => order[a.severity] - order[b.severity]);
    return { statements: triggered, triggered: triggered.length, totalChecked: this.rules.length, lastUpdated: trends.lastUpdated };
  }
}
