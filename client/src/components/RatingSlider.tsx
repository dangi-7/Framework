import { Slider } from "@/components/ui/slider";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { GraduationCap, Smartphone, Sparkles, Zap, BarChart3 } from "lucide-react";

interface RatingSliderProps {
  category: {
    id: string;
    name: string;
    description: string;
    icon: string;
  };
  value: number;
  onChange: (value: number) => void;
}

const iconMap: Record<string, any> = {
  AcademicCap: GraduationCap,
  DeviceMobile: Smartphone,
  Sparkles: Sparkles,
  Bolt: Zap,
  ChartBar: BarChart3,
};

const ratingLabels = ["Poor", "Fair", "Good", "Very Good", "Excellent"];
const ratingColors = [
  "text-destructive",
  "text-chart-3",
  "text-chart-3",
  "text-chart-2",
  "text-chart-2"
];

export default function RatingSlider({ category, value, onChange }: RatingSliderProps) {
  const Icon = iconMap[category.icon] || BarChart3;
  const colorClass = ratingColors[value - 1] || "text-muted-foreground";

  return (
    <Card className="hover-elevate transition-all" data-testid={`card-rating-${category.id}`}>
      <CardHeader className="space-y-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-card-border flex items-center justify-center flex-shrink-0">
            <Icon className="h-6 w-6 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <CardTitle className="text-xl mb-1">{category.name}</CardTitle>
            <CardDescription className="text-sm leading-relaxed">
              {category.description}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Rating</span>
            <span className={`text-2xl font-bold font-mono ${colorClass}`} data-testid={`text-rating-value-${category.id}`}>
              {value}/5
            </span>
          </div>
          
          <Slider
            value={[value]}
            onValueChange={(values) => onChange(values[0])}
            min={1}
            max={5}
            step={1}
            className="w-full"
            data-testid={`slider-${category.id}`}
          />
          
          <div className="flex justify-between text-xs text-muted-foreground">
            {ratingLabels.map((label, index) => (
              <span 
                key={index}
                className={value === index + 1 ? colorClass + " font-semibold" : ""}
              >
                {label}
              </span>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
