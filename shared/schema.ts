import { sql } from "drizzle-orm";
import { pgTable, text, varchar, integer, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// Educational App Evaluation Schema
export const evaluations = pgTable("evaluations", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  appName: text("app_name").notNull(),
  
  // 5 Rating Categories (1-5 scale)
  pedagogicalDesign: integer("pedagogical_design").notNull(),
  uiUx: integer("ui_ux").notNull(),
  engagement: integer("engagement").notNull(),
  technicalPerformance: integer("technical_performance").notNull(),
  learningEffectiveness: integer("learning_effectiveness").notNull(),
  
  // Computed Quality Score (percentage)
  qualityScore: integer("quality_score").notNull(),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertEvaluationSchema = createInsertSchema(evaluations).omit({
  id: true,
  createdAt: true,
});

export type InsertEvaluation = z.infer<typeof insertEvaluationSchema>;
export type Evaluation = typeof evaluations.$inferSelect;

// Rating categories configuration
export const RATING_CATEGORIES = [
  {
    id: 'pedagogicalDesign',
    name: 'Pedagogical Design',
    description: 'Educational methodology, learning theories, curriculum alignment',
    icon: 'AcademicCap',
  },
  {
    id: 'uiUx',
    name: 'User Interface & Experience',
    description: 'Visual design, navigation, accessibility, user-friendliness',
    icon: 'DeviceMobile',
  },
  {
    id: 'engagement',
    name: 'Engagement & Motivation',
    description: 'Gamification, rewards, feedback mechanisms, user retention',
    icon: 'Sparkles',
  },
  {
    id: 'technicalPerformance',
    name: 'Technical Performance',
    description: 'Speed, reliability, compatibility, security, data privacy',
    icon: 'Bolt',
  },
  {
    id: 'learningEffectiveness',
    name: 'Learning Effectiveness',
    description: 'Knowledge retention, skill development, measurable outcomes',
    icon: 'ChartBar',
  },
] as const;
