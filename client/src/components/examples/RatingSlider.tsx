import { useState } from 'react';
import RatingSlider from '../RatingSlider';

export default function RatingSliderExample() {
  const [rating, setRating] = useState(3);
  
  const category = {
    id: 'pedagogicalDesign',
    name: 'Pedagogical Design',
    description: 'Educational methodology, learning theories, curriculum alignment',
    icon: 'AcademicCap',
  };

  return (
    <div className="p-6 max-w-2xl">
      <RatingSlider 
        category={category}
        value={rating}
        onChange={setRating}
      />
    </div>
  );
}
