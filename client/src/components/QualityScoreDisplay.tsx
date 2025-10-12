interface QualityScoreDisplayProps {
  score: number;
}

export default function QualityScoreDisplay({ score }: QualityScoreDisplayProps) {
  const getScoreColor = (score: number) => {
    if (score >= 75) return "text-chart-2";
    if (score >= 50) return "text-chart-3";
    return "text-destructive";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    if (score >= 40) return "Fair";
    return "Needs Improvement";
  };

  const circumference = 2 * Math.PI * 120;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center space-y-6">
      <div className="relative w-64 h-64">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 256 256">
          {/* Background circle */}
          <circle
            cx="128"
            cy="128"
            r="120"
            fill="none"
            stroke="hsl(var(--card-border))"
            strokeWidth="16"
          />
          {/* Progress circle */}
          <circle
            cx="128"
            cy="128"
            r="120"
            fill="none"
            stroke={`hsl(var(--chart-${score >= 75 ? '2' : score >= 50 ? '3' : 'destructive'}))`}
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        
        {/* Score text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className={`text-6xl font-bold font-mono ${getScoreColor(score)}`} data-testid="text-quality-score">
            {Math.round(score)}%
          </div>
          <div className="text-sm text-muted-foreground mt-2">Quality Score</div>
        </div>
      </div>

      <div className="text-center space-y-2">
        <div className={`text-2xl font-semibold ${getScoreColor(score)}`} data-testid="text-score-label">
          {getScoreLabel(score)}
        </div>
        <p className="text-sm text-muted-foreground max-w-md">
          {score >= 75 
            ? "This educational app demonstrates excellent quality across all evaluated parameters."
            : score >= 50
            ? "This app shows good potential with room for targeted improvements."
            : "Significant improvements needed to meet educational quality standards."}
        </p>
      </div>
    </div>
  );
}
