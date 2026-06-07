class ClimatePredict {
  constructor(city) {
    this.city = city;
  }

  async fetchYearData(year, startMonth, endMonth) {
    const start = `${year}-${String(startMonth).padStart(2, '0')}-01`;
    const end = endMonth === 2 ? `${year}-02-28` : `${year}-${String(endMonth).padStart(2, '0')}-${new Date(year, endMonth, 0).getDate()}`;
    const url = `${APP.HISTORICAL_API}?latitude=${this.city.lat}&longitude=${this.city.lon}&start_date=${start}&end_date=${end}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Historical API error: ${res.status}`);
    return (await res.json()).daily;
  }

  async fetchMultiYear(years, startMonth, endMonth) {
    const results = [];
    for (const year of years) {
      const daily = await this.fetchYearData(year, startMonth, endMonth);
      const maxes = daily.temperature_2m_max.filter(v => v !== null);
      const mins = daily.temperature_2m_min.filter(v => v !== null);
      const precip = daily.precipitation_sum.filter(v => v !== null);
      results.push({
        year,
        maxTemp: Math.max(...maxes),
        minTemp: Math.min(...mins),
        avgMax: maxes.reduce((a, b) => a + b, 0) / maxes.length,
        avgMin: mins.reduce((a, b) => a + b, 0) / mins.length,
        totalPrecip: precip.reduce((a, b) => a + b, 0),
        daysAbove: t => maxes.filter(v => v >= t).length,
      });
    }
    return results;
  }

  linearRegression(values) {
    const n = values.length;
    const idx = values.map((_, i) => i);
    const sumX = idx.reduce((a, b) => a + b, 0);
    const sumY = values.reduce((a, b) => a + b, 0);
    const sumXY = idx.reduce((s, i) => s + i * values[i], 0);
    const sumX2 = idx.reduce((s, i) => s + i * i, 0);
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    const yHat = idx.map(i => slope * i + intercept);
    const ssRes = values.reduce((s, v, i) => s + (v - yHat[i]) ** 2, 0);
    const ssTot = values.reduce((s, v) => s + (v - sumY / n) ** 2, 0);
    return { slope, intercept, rSquared: 1 - ssRes / ssTot, yHat };
  }

  async computeTrends(years, startMonth, endMonth) {
    const yearlyData = await this.fetchMultiYear(years, startMonth, endMonth);
    const avgMaxes = yearlyData.map(d => d.avgMax);
    const avgMaxTrend = this.linearRegression(avgMaxes);
    const hotDays35 = yearlyData.map(d => d.daysAbove(APP.THRESHOLDS.TEMP_WARN));
    const hotDays40 = yearlyData.map(d => d.daysAbove(APP.THRESHOLDS.TEMP_DANGER));
    const hotDays43 = yearlyData.map(d => d.daysAbove(APP.THRESHOLDS.TEMP_CRITICAL));
    const hotDays45 = yearlyData.map(d => d.daysAbove(APP.THRESHOLDS.TEMP_EXTREME));
    const currentYear = yearlyData[yearlyData.length - 1];
    const previousYear = yearlyData[yearlyData.length - 2];
    const delta = currentYear.avgMax - previousYear.avgMax;
    let consecutiveHot = 0;
    for (let i = yearlyData.length - 1; i >= 0; i--) {
      if (yearlyData[i].daysAbove(APP.THRESHOLDS.TEMP_DANGER) > 0) consecutiveHot++; else break;
    }
    return {
      city: this.city,
      yearlyData,
      trends: { avgMax: avgMaxTrend, hotDays35: this.linearRegression(hotDays35), hotDays40: this.linearRegression(hotDays40) },
      currentYear, previousYear, delta,
      consecutiveHotYears: consecutiveHot,
      warmingRatePerYear: Math.abs(avgMaxTrend.slope),
      hotDaysCounts: { above35: hotDays35, above40: hotDays40, above43: hotDays43, above45: hotDays45 },
      lastUpdated: new Date().toISOString(),
    };
  }
}
