// Medical system type definitions

export interface Procedure {
  id: string;
  name: string;
  description: string;
  category: 'Cirurgia' | 'Consulta' | 'Exame' | 'Curativo' | 'Quimioterapia' | 'Outros';
  isHighCost: boolean;
  estimatedDuration: number; // minutes
  createdAt: string;
  createdBy: string;
}

export interface ProcedureExecution {
  id: string;
  procedureId: string;
  procedureName: string;
  procedureType: string;
  patientWallet: string;
  professionalWallet: string;
  professionalName?: string;
  professionalRegistry?: string;
  executedAt: string;
  materials?: MaterialUsage[];
  isHighCostMaterials: boolean;
  status: 'Em Andamento' | 'Concluído' | 'Cancelado';
}

export interface MaterialUsage {
  itemId: string;
  itemName: string;
  quantity: number;
  lot: string;
  isHighCost: boolean;
}

export interface Professional {
  wallet: string;
  name: string;
  category: string;
  registroConselho: string;
  hospitalId: string;
  isActive: boolean;
}

export interface Patient {
  wallet: string;
  name: string;
  cpf: string;
}

export interface BlockchainEvent {
  id: string;
  type: 'PROCEDURE_REGISTERED' | 'HIGH_COST_MATERIAL_USED' | 'PROCEDURE_COMPLETED';
  timestamp: string;
  data: any;
  blockNumber: number;
  transactionHash: string;
}

export interface AlertNotification {
  id: string;
  type: 'HIGH_COST_PROCEDURE' | 'CRITICAL_MATERIAL' | 'SYSTEM_ALERT';
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  severity: 'low' | 'medium' | 'high' | 'critical';
  relatedProcedure?: ProcedureExecution;
}