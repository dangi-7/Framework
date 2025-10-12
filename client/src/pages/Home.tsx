import Navigation from "@/components/Navigation";
import HeroSection from "@/components/HeroSection";
import FeatureCards from "@/components/FeatureCards";
import { Card, CardContent } from "@/components/ui/card";
import { BarChart3, FileText, Download } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />
      <main className="flex-1">
        <HeroSection />
        <FeatureCards />
        
        {/* How it works section */}
        <div className="bg-card-border/30 py-20">
          <div className="container mx-auto px-6">
            <div className="text-center mb-12 space-y-4">
              <h2 className="text-4xl font-bold">How It Works</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Simple three-step process to evaluate any educational app
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {[
                {
                  icon: FileText,
                  step: "01",
                  title: "Fill Evaluation Form",
                  description: "Rate the app across 5 key categories using our intuitive slider interface"
                },
                {
                  icon: BarChart3,
                  step: "02",
                  title: "View Results",
                  description: "Get instant quality score with detailed charts and performance breakdown"
                },
                {
                  icon: Download,
                  step: "03",
                  title: "Download Report",
                  description: "Export comprehensive PDF report with insights and recommendations"
                }
              ].map((item, index) => {
                const Icon = item.icon;
                return (
                  <Card key={index} className="text-center hover-elevate transition-all">
                    <CardContent className="pt-8 pb-6 space-y-4">
                      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-2">
                        <Icon className="h-8 w-8 text-primary" />
                      </div>
                      <div className="text-sm font-mono text-primary font-bold">{item.step}</div>
                      <h3 className="text-xl font-semibold">{item.title}</h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {item.description}
                      </p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </div>

        {/* CTA section */}
        <div className="py-20">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Evaluate Your Educational App?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Start your comprehensive quality assessment now
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-6 text-center text-sm text-muted-foreground">
          <p>© 2025 EduApp QA. Quality Assurance for Educational App Design.</p>
        </div>
      </footer>
    </div>
  );
}
