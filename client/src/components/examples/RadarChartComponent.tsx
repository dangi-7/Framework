import RadarChartComponent from '../RadarChartComponent';

export default function RadarChartComponentExample() {
  const data = [
    { category: 'Pedagogical', value: 4, fullMark: 5 },
    { category: 'UI/UX', value: 3, fullMark: 5 },
    { category: 'Engagement', value: 5, fullMark: 5 },
    { category: 'Technical', value: 4, fullMark: 5 },
    { category: 'Learning', value: 4, fullMark: 5 },
  ];

  return (
    <div className="p-6 max-w-3xl">
      <RadarChartComponent data={data} />
    </div>
  );
}
