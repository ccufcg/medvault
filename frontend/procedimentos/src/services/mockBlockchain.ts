import { BlockchainEvent, ProcedureExecution, Professional } from '@/types/medical';

class MockBlockchainService {
  private listeners: Array<(event: BlockchainEvent) => void> = [];
  private isListening = false;
  private eventInterval?: NodeJS.Timeout;

  // mock data
  private mockProcedures: ProcedureExecution[] = [
    {
      id: "proc_001",
      procedureId: "type_001",
      procedureName: "Sessão de Quimioterapia",
      procedureType: "Quimioterapia",
      patientWallet: "0xPac...iEnte1",
      professionalWallet: "0xABC...123",
      professionalName: "Dr. Gabriel Santos",
      professionalRegistry: "CRM/PB 12345",
      executedAt: new Date().toISOString(),
      materials: [
        {
          itemId: "mat_5501",
          itemName: "Medicamento Oncológico Premium",
          quantity: 2,
          lot: "LOTE-XYZ-2025",
          isHighCost: true
        }
      ],
      isHighCostMaterials: true,
      status: "Em Andamento"
    }
  ];

  private mockProfessionals: Professional[] = [
    {
      wallet: "0xABC...123",
      name: "Dr. Gabriel Santos",
      category: "Médico",
      registroConselho: "CRM/PB 12345",
      hospitalId: "HSP001",
      isActive: true
    },
    {
      wallet: "0xDEF...456",
      name: "Dra. Maria Silva", 
      category: "Enfermeira",
      registroConselho: "COREN/PB 67890",
      hospitalId: "HSP001",
      isActive: true
    }
  ];

  startListening() {
    if (this.isListening) return;
    
    this.isListening = true;
    console.log("🔗 Blockchain listener iniciado - Monitorando eventos médicos em tempo real");

    // Simula eventos aleatórios de blockchain
    this.eventInterval = setInterval(() => {
      if (Math.random() > 0.7) { // 30% chance de evento
        this.simulateRandomEvent();
      }
    }, 8000); // Evento a cada 8 segundos
  }

  stopListening() {
    this.isListening = false;
    if (this.eventInterval) {
      clearInterval(this.eventInterval);
    }
    console.log("🔗 Blockchain listener parado");
  }

  subscribe(callback: (event: BlockchainEvent) => void) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }

  private simulateRandomEvent() {
    const eventTypes = ['PROCEDURE_REGISTERED', 'HIGH_COST_MATERIAL_USED', 'PROCEDURE_COMPLETED'] as const;
    const randomType = eventTypes[Math.floor(Math.random() * eventTypes.length)];
    
    const event: BlockchainEvent = {
      id: `event_${Date.now()}`,
      type: randomType,
      timestamp: new Date().toISOString(),
      blockNumber: Math.floor(Math.random() * 1000000) + 100000,
      transactionHash: `0x${Math.random().toString(16).substr(2, 64)}`,
      data: this.generateEventData(randomType)
    };

    console.log("🚨 Novo evento blockchain detectado:", event);
    this.notifyListeners(event);
  }

  private generateEventData(type: BlockchainEvent['type']) {
    const randomProc = this.mockProcedures[Math.floor(Math.random() * this.mockProcedures.length)];
    const randomProf = this.mockProfessionals[Math.floor(Math.random() * this.mockProfessionals.length)];

    switch (type) {
      case 'HIGH_COST_MATERIAL_USED':
        return {
          procedureId: randomProc.id,
          procedureName: randomProc.procedureName,
          patientWallet: `0xPac...${Math.random().toString(16).substr(2, 6)}`,
          professionalWallet: randomProf.wallet,
          professionalName: randomProf.name,
          professionalRegistry: randomProf.registroConselho,
          materials: randomProc.materials,
          timestamp: new Date().toISOString()
        };
      
      case 'PROCEDURE_REGISTERED':
        return {
          procedureId: `proc_${Date.now()}`,
          procedureName: randomProc.procedureName,
          patientWallet: `0xPac...${Math.random().toString(16).substr(2, 6)}`,
          professionalWallet: randomProf.wallet,
          timestamp: new Date().toISOString()
        };
      
      case 'PROCEDURE_COMPLETED':
        return {
          procedureId: randomProc.id,
          patientWallet: randomProc.patientWallet,
          professionalWallet: randomProf.wallet,
          completedAt: new Date().toISOString()
        };
      
      default:
        return {};
    }
  }

  private notifyListeners(event: BlockchainEvent) {
    this.listeners.forEach(listener => {
      try {
        listener(event);
      } catch (error) {
        console.error("Erro ao notificar listener:", error);
      }
    });
  }

  async getAllProcedures(): Promise<ProcedureExecution[]> {
    return [...this.mockProcedures];
  }

  async getProceduresByProfessional(wallet: string): Promise<ProcedureExecution[]> {
    return this.mockProcedures.filter(proc => proc.professionalWallet === wallet);
  }

  async getAllProfessionals(): Promise<Professional[]> {
    return [...this.mockProfessionals];
  }

  simulateHighCostProcedure() {
    const event: BlockchainEvent = {
      id: `event_${Date.now()}`,
      type: 'HIGH_COST_MATERIAL_USED',
      timestamp: new Date().toISOString(),
      blockNumber: Math.floor(Math.random() * 1000000) + 100000,
      transactionHash: `0x${Math.random().toString(16).substr(2, 64)}`,
      data: {
        procedureId: "proc_urgent_001",
        procedureName: "Cirurgia Cardíaca de Emergência",
        patientWallet: `0xEmr...${Math.random().toString(16).substr(2, 6)}`,
        professionalWallet: this.mockProfessionals[0].wallet,
        professionalName: this.mockProfessionals[0].name,
        professionalRegistry: this.mockProfessionals[0].registroConselho,
        materials: [
          {
            itemId: "mat_9999",
            itemName: "Marca-passo Premium Importado",
            quantity: 1,
            lot: "LOTE-URGENT-2025",
            isHighCost: true
          }
        ],
        timestamp: new Date().toISOString()
      }
    };

    console.log("🚨 ALERTA: Procedimento de alto custo simulado!", event);
    this.notifyListeners(event);
  }
}

export const blockchainService = new MockBlockchainService();