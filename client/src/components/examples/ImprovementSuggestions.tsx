import ImprovementSuggestions from '../ImprovementSuggestions';

export default function ImprovementSuggestionsExample() {
  const suggestions = [
    {
      category: 'Pedagogical Design',
      score: 4,
      suggestions: [
        'Continue leveraging evidence-based learning theories',
        'Consider adding adaptive learning pathways'
      ]
    },
    {
      category: 'UI/UX',
      score: 3,
      suggestions: [
        'Improve navigation clarity with breadcrumbs',
        'Enhance color contrast for better accessibility',
        'Add onboarding tutorials for new users'
      ]
    },
    {
      category: 'Engagement',
      score: 5,
      suggestions: [
        'Excellent gamification implementation',
        'Strong user retention mechanisms in place'
      ]
    }
  ];

  return (
    <div className="p-6 max-w-3xl">
      <ImprovementSuggestions suggestions={suggestions} />
    </div>
  );
}
