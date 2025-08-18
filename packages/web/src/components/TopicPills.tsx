import { FC } from 'react';

interface TopicPillsProps {
  onTopicClick: (topic: string) => void;
}

const GRADE_4_SCIENCE_TOPICS = [
  { id: 'light', label: '💡 Light', prompt: 'Can you help me understand how light works?' },
  { id: 'sound', label: '🔊 Sound', prompt: 'Tell me about sound and vibrations' },
  { id: 'structures', label: '🏗️ Structures', prompt: 'How do structures stay strong?' },
  { id: 'habitats', label: '🦌 Habitats', prompt: 'What are habitats and ecosystems?' },
  { id: 'rocks', label: '🪨 Rocks', prompt: 'Can you explain rocks and minerals?' },
  { id: 'pulleys', label: '⚙️ Pulleys', prompt: 'How do pulleys and gears work?' },
];

const TopicPills: FC<TopicPillsProps> = ({ onTopicClick }) => {
  return (
    <div className="px-4 py-3 bg-gradient-to-r from-purple-50 to-blue-50 border-b border-gray-200">
      <p className="text-xs text-gray-600 font-medium mb-2">Quick Topics - Grade 4 Science</p>
      <div className="flex flex-wrap gap-2">
        {GRADE_4_SCIENCE_TOPICS.map((topic) => (
          <button
            key={topic.id}
            onClick={() => onTopicClick(topic.prompt)}
            className="px-3 py-1.5 text-sm font-medium rounded-full bg-white text-purple-700 border border-purple-200 hover:bg-purple-50 hover:border-purple-300 transition-colors duration-200 shadow-sm hover:shadow"
          >
            {topic.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TopicPills;