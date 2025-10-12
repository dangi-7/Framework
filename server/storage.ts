import { type Evaluation, type InsertEvaluation } from "@shared/schema";
import { randomUUID } from "crypto";

// Storage interface for educational app evaluations
export interface IStorage {
  getEvaluation(id: string): Promise<Evaluation | undefined>;
  createEvaluation(evaluation: InsertEvaluation): Promise<Evaluation>;
  getAllEvaluations(): Promise<Evaluation[]>;
}

export class MemStorage implements IStorage {
  private evaluations: Map<string, Evaluation>;

  constructor() {
    this.evaluations = new Map();
  }

  async getEvaluation(id: string): Promise<Evaluation | undefined> {
    return this.evaluations.get(id);
  }

  async createEvaluation(insertEvaluation: InsertEvaluation): Promise<Evaluation> {
    const id = randomUUID();
    const evaluation: Evaluation = { 
      ...insertEvaluation, 
      id,
      createdAt: new Date()
    };
    this.evaluations.set(id, evaluation);
    return evaluation;
  }

  async getAllEvaluations(): Promise<Evaluation[]> {
    return Array.from(this.evaluations.values());
  }
}

export const storage = new MemStorage();
