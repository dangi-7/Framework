import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Lightbulb, AlertCircle, CheckCircle2 } from "lucide-react";

interface Suggestion {
  category: string;
  score: number;
  suggestions: string[];
}

interface ImprovementSuggestionsProps {
  suggestions: Suggestion[];
}

export default function ImprovementSuggestions({ suggestions }: ImprovementSuggestionsProps) {
  const getSuggestionIcon = (score: number) => {
    if (score >= 4) return <CheckCircle2 className="h-5 w-5 text-chart-2" />;
    if (score >= 3) return <Lightbulb className="h-5 w-5 text-chart-3" />;
    return <AlertCircle className="h-5 w-5 text-destructive" />;
  };

  const getSuggestionPriority = (score: number) => {
    if (score >= 4) return "Excellent";
    if (score >= 3) return "Enhancement Opportunities";
    return "Critical Improvements Needed";
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-primary" />
          AI-Powered Improvement Suggestions
        </CardTitle>
        <CardDescription>
          Actionable recommendations to enhance your educational app quality
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {suggestions.map((item, index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger className="hover:no-underline" data-testid={`accordion-trigger-${index}`}>
                <div className="flex items-center gap-3 text-left">
                  {getSuggestionIcon(item.score)}
                  <div>
                    <div className="font-semibold">{item.category}</div>
                    <div className="text-sm text-muted-foreground">
                      {getSuggestionPriority(item.score)}
                    </div>
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <ul className="space-y-3 mt-2 ml-8">
                  {item.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex gap-3 text-sm leading-relaxed">
                      <span className="text-primary mt-1">•</span>
                      <span className="flex-1">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  );
}
