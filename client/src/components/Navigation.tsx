import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Home, FileText, BarChart3 } from "lucide-react";

export default function Navigation() {
  const [location] = useLocation();

  const navItems = [
    { path: "/", label: "Home", icon: Home },
    { path: "/evaluate", label: "Evaluate", icon: FileText },
    { path: "/report", label: "Results", icon: BarChart3 },
  ];

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-6">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" data-testid="link-home">
            <div className="flex items-center gap-2 text-xl font-bold hover-elevate active-elevate-2 px-3 py-2 rounded-lg transition-all cursor-pointer">
              <BarChart3 className="h-6 w-6 text-primary" />
              <span className="hidden sm:inline">EduApp QA</span>
            </div>
          </Link>

          <div className="flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location === item.path;
              
              return (
                <Link key={item.path} href={item.path}>
                  <Button
                    variant={isActive ? "secondary" : "ghost"}
                    size="sm"
                    className="gap-2"
                    asChild
                    data-testid={`button-nav-${item.label.toLowerCase()}`}
                  >
                    <div>
                      <Icon className="h-4 w-4" />
                      <span className="hidden sm:inline">{item.label}</span>
                    </div>
                  </Button>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
