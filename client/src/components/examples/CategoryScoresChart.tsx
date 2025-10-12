import CategoryScoresChart from '../CategoryScoresChart';

export default function CategoryScoresChartExample() {
  const data = [
    { name: 'Pedagogical', score: 4 },
    { name: 'UI/UX', score: 3 },
    { name: 'Engagement', score: 5 },
    { name: 'Technical', score: 4 },
    { name: 'Learning', score: 4 },
  ];

  return (
    <div className="p-6 max-w-3xl">
      <CategoryScoresChart data={data} />
    </div>
  );
}
