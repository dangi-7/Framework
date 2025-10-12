import { useState } from "react";
import Navigation from "@/components/Navigation";
import QualityScoreDisplay from "@/components/QualityScoreDisplay";
import RadarChartComponent from "@/components/RadarChartComponent";
import CategoryScoresChart from "@/components/CategoryScoresChart";
import ImprovementSuggestions from "@/components/ImprovementSuggestions";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Download, RefreshCw, Loader2 } from "lucide-react";
import { Link } from "wouter";
import jsPDF from 'jspdf';

export default function Report() {
  const [isDownloading, setIsDownloading] = useState(false);

  // TODO: Remove mock functionality - this will come from actual evaluation data
  const mockData = {
    appName: "Sample Educational App",
    qualityScore: 78,
    ratings: {
      pedagogicalDesign: 4,
      uiUx: 3,
      engagement: 5,
      technicalPerformance: 4,
      learningEffectiveness: 4,
    },
    date: new Date().toLocaleDateString(),
  };

  const radarData = [
    { category: 'Pedagogical', value: mockData.ratings.pedagogicalDesign, fullMark: 5 },
    { category: 'UI/UX', value: mockData.ratings.uiUx, fullMark: 5 },
    { category: 'Engagement', value: mockData.ratings.engagement, fullMark: 5 },
    { category: 'Technical', value: mockData.ratings.technicalPerformance, fullMark: 5 },
    { category: 'Learning', value: mockData.ratings.learningEffectiveness, fullMark: 5 },
  ];

  const barData = [
    { name: 'Pedagogical', score: mockData.ratings.pedagogicalDesign },
    { name: 'UI/UX', score: mockData.ratings.uiUx },
    { name: 'Engagement', score: mockData.ratings.engagement },
    { name: 'Technical', score: mockData.ratings.technicalPerformance },
    { name: 'Learning', score: mockData.ratings.learningEffectiveness },
  ];

  const suggestions = [
    {
      category: 'Pedagogical Design',
      score: mockData.ratings.pedagogicalDesign,
      suggestions: [
        'Continue leveraging evidence-based learning theories and best practices',
        'Consider adding adaptive learning pathways to personalize student experiences',
        'Integrate formative assessments throughout the learning journey'
      ]
    },
    {
      category: 'User Interface & Experience',
      score: mockData.ratings.uiUx,
      suggestions: [
        'Improve navigation clarity by implementing breadcrumbs and clear hierarchy',
        'Enhance color contrast ratios to meet WCAG 2.1 AA accessibility standards',
        'Add interactive onboarding tutorials for first-time users',
        'Optimize touch targets for mobile devices (minimum 44x44px)'
      ]
    },
    {
      category: 'Engagement & Motivation',
      score: mockData.ratings.engagement,
      suggestions: [
        'Excellent gamification implementation - maintain current approach',
        'Strong user retention mechanisms are in place',
        'Consider adding social features for peer collaboration'
      ]
    },
    {
      category: 'Technical Performance',
      score: mockData.ratings.technicalPerformance,
      suggestions: [
        'Maintain robust security protocols and regular audits',
        'Consider implementing progressive web app (PWA) capabilities',
        'Optimize image and media loading for slower connections'
      ]
    },
    {
      category: 'Learning Effectiveness',
      score: mockData.ratings.learningEffectiveness,
      suggestions: [
        'Implement detailed analytics to track learning outcomes',
        'Add spaced repetition algorithms for better knowledge retention',
        'Provide clear progress tracking and achievement milestones'
      ]
    }
  ];

  const handleDownloadPDF = async () => {
    setIsDownloading(true);
    console.log("Generating PDF report...");

    // TODO: Remove mock functionality - generate actual PDF with charts
    setTimeout(() => {
      const doc = new jsPDF();
      
      // Title
      doc.setFontSize(20);
      doc.text('Educational App Quality Assessment', 20, 20);
      
      // App info
      doc.setFontSize(12);
      doc.text(`App Name: ${mockData.appName}`, 20, 35);
      doc.text(`Date: ${mockData.date}`, 20, 42);
      doc.text(`Quality Score: ${mockData.qualityScore}%`, 20, 49);
      
      // Category scores
      doc.setFontSize(14);
      doc.text('Category Scores', 20, 65);
      doc.setFontSize(11);
      let yPos = 75;
      barData.forEach((item) => {
        doc.text(`${item.name}: ${item.score}/5`, 25, yPos);
        yPos += 7;
      });
      
      // Recommendations
      doc.setFontSize(14);
      doc.text('Improvement Recommendations', 20, yPos + 10);
      doc.setFontSize(10);
      yPos += 20;
      
      suggestions.forEach((item) => {
        if (yPos > 270) {
          doc.addPage();
          yPos = 20;
        }
        doc.setFontSize(11);
        doc.text(item.category, 20, yPos);
        yPos += 7;
        doc.setFontSize(9);
        item.suggestions.forEach((suggestion) => {
          const lines = doc.splitTextToSize(`• ${suggestion}`, 170);
          lines.forEach((line: string) => {
            if (yPos > 280) {
              doc.addPage();
              yPos = 20;
            }
            doc.text(line, 25, yPos);
            yPos += 5;
          });
        });
        yPos += 5;
      });
      
      doc.save(`${mockData.appName.replace(/\s+/g, '_')}_QA_Report.pdf`);
      setIsDownloading(false);
      console.log("PDF downloaded successfully");
    }, 1000);
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navigation />
      
      <main className="flex-1 py-12">
        <div className="container mx-auto px-6 max-w-6xl">
          {/* Header */}
          <div className="mb-8 space-y-4">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="space-y-2">
                <h1 className="text-4xl font-bold" data-testid="text-report-title">
                  Evaluation Report
                </h1>
                <p className="text-lg text-muted-foreground">
                  {mockData.appName} • {mockData.date}
                </p>
              </div>
              <div className="flex gap-3">
                <Button 
                  variant="outline" 
                  className="gap-2"
                  onClick={handleDownloadPDF}
                  disabled={isDownloading}
                  data-testid="button-download-pdf"
                >
                  {isDownloading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Download className="h-4 w-4" />
                      Download PDF
                    </>
                  )}
                </Button>
                <Link href="/evaluate">
                  <Button className="gap-2" data-testid="button-new-evaluation">
                    <RefreshCw className="h-4 w-4" />
                    New Evaluation
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          {/* Quality Score Display */}
          <Card className="mb-8">
            <CardContent className="pt-8 pb-8">
              <QualityScoreDisplay score={mockData.qualityScore} />
            </CardContent>
          </Card>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <RadarChartComponent data={radarData} />
            <CategoryScoresChart data={barData} />
          </div>

          {/* Individual Category Scores */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Detailed Category Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {barData.map((item, index) => {
                  const scorePercent = (item.score / 5) * 100;
                  const colorClass = item.score >= 4 ? "text-chart-2" : item.score >= 3 ? "text-chart-3" : "text-destructive";
                  
                  return (
                    <div key={index} className="space-y-2">
                      <div className="text-sm font-medium text-muted-foreground">{item.name}</div>
                      <div className={`text-3xl font-bold font-mono ${colorClass}`}>
                        {item.score}/5
                      </div>
                      <div className="h-2 bg-card-border rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${item.score >= 4 ? "bg-chart-2" : item.score >= 3 ? "bg-chart-3" : "bg-destructive"} rounded-full transition-all`}
                          style={{ width: `${scorePercent}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Improvement Suggestions */}
          <ImprovementSuggestions suggestions={suggestions} />
        </div>
      </main>
    </div>
  );
}
