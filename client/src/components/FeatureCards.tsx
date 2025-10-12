import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { GraduationCap, Smartphone, Sparkles, Zap, BarChart3 } from "lucide-react";

const features = [
  {
    icon: GraduationCap,
    title: "Pedagogical Design",
    description: "Assess educational methodology, learning theories, and curriculum alignment",
    color: "text-chart-1",
  },
  {
    icon: Smartphone,
    title: "UI/UX Excellence",
    description: "Evaluate visual design, navigation, accessibility, and user-friendliness",
    color: "text-chart-2",
  },
  {
    icon: Sparkles,
    title: "Engagement & Motivation",
    description: "Measure gamification, rewards, feedback mechanisms, and user retention",
    color: "text-chart-3",
  },
  {
    icon: Zap,
    title: "Technical Performance",
    description: "Analyze speed, reliability, compatibility, security, and data privacy",
    color: "text-chart-4",
  },
  {
    icon: BarChart3,
    title: "Learning Effectiveness",
    description: "Track knowledge retention, skill development, and measurable outcomes",
    color: "text-chart-5",
  },
];

export default function FeatureCards() {
  return (
    <div className="container mx-auto px-6 py-20">
      <div className="text-center mb-12 space-y-4">
        <h2 className="text-4xl font-bold" data-testid="text-features-title">
          Comprehensive Evaluation Framework
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Our platform evaluates educational apps across five critical dimensions
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <Card 
              key={index} 
              className="hover-elevate transition-all duration-300"
              data-testid={`card-feature-${index}`}
            >
              <CardHeader className="space-y-4">
                <div className={`w-12 h-12 rounded-lg bg-card-border flex items-center justify-center ${feature.color}`}>
                  <Icon className="h-6 w-6" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
