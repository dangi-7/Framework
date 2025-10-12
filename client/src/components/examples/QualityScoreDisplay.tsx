import QualityScoreDisplay from '../QualityScoreDisplay';

export default function QualityScoreDisplayExample() {
  return (
    <div className="p-8 flex items-center justify-center">
      <QualityScoreDisplay score={78} />
    </div>
  );
}
