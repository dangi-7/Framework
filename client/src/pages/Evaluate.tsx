import { useState } from "react";
import { useLocation } from "wouter";
import Navigation from "@/components/Navigation";
import RatingSlider from "@/components/RatingSlider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, Loader2 } from "lucide-react";
import { RATING_CATEGORIES } from "@shared/schema";

export default function Evaluate() {
  const [, setLocation] = useLocation();
  const [appName, setAppName] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [ratings, setRatings] = useState({
    pedagogicalDesign: 3,
    uiUx: 3,
    engagement: 3,
    technicalPerformance: 3,
    learningEffectiveness: 3,
  });

  const handleRatingChange = (categoryId: string, value: number) => {
    setRatings(prev => ({ ...prev, [categoryId]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!appName.trim()) {
      console.log("App name is required");
      return;
    }

    console.log("Submitting evaluation:", { appName, ratings });
    setIsSubmitting(true);

    // TODO: Remove mock functionality - simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setLocation("/report");
    }, 1500);
  };

  const calculateProgress = () => {
    const totalPossible = Object.keys(ratings).length * 5;
    const currentTotal = Object.values(ratings).reduce((sum, val) => sum + val, 0);
    return Math.round((currentTotal / totalPossible) * 100);
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navigation />
      
      <main className="flex-1 py-12">
        <div className="container mx-auto px-6 max-w-4xl">
          <div className="mb-8 space-y-4">
            <h1 className="text-4xl font-bold" data-testid="text-evaluate-title">
              Evaluate Educational App
            </h1>
            <p className="text-lg text-muted-foreground">
              Rate the app across 5 comprehensive categories to generate a detailed quality assessment
            </p>
          </div>

          {/* Progress indicator */}
          <Card className="mb-8">
            <CardContent className="pt-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Overall Progress</span>
                  <span className="font-mono font-semibold text-primary">{calculateProgress()}%</span>
                </div>
                <div className="h-2 bg-card-border rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary transition-all duration-500 rounded-full"
                    style={{ width: `${calculateProgress()}%` }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* App name input */}
            <Card>
              <CardHeader>
                <CardTitle>App Information</CardTitle>
                <CardDescription>Enter the name of the educational app you're evaluating</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Label htmlFor="appName">App Name *</Label>
                  <Input
                    id="appName"
                    placeholder="e.g., Duolingo, Khan Academy, Photomath..."
                    value={appName}
                    onChange={(e) => setAppName(e.target.value)}
                    required
                    data-testid="input-app-name"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Rating categories */}
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Evaluation Categories</h2>
              {RATING_CATEGORIES.map((category) => (
                <RatingSlider
                  key={category.id}
                  category={category}
                  value={ratings[category.id as keyof typeof ratings]}
                  onChange={(value) => handleRatingChange(category.id, value)}
                />
              ))}
            </div>

            {/* Submit button */}
            <div className="flex justify-end pt-6">
              <Button 
                type="submit" 
                size="lg" 
                className="gap-2"
                disabled={isSubmitting}
                data-testid="button-submit-evaluation"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating Report...
                  </>
                ) : (
                  <>
                    Generate Report
                    <ArrowRight className="h-5 w-5" />
                  </>
                )}
              </Button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
