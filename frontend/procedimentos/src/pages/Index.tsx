import { useState } from 'react';
import { MonitoringDashboard } from '@/components/medical/MonitoringDashboard';
import { ProcedureTypeForm } from '@/components/medical/ProcedureTypeForm';
import { ProcedureTypesList } from '@/components/medical/ProcedureTypesList';
import { Procedure } from '@/types/medical';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Activity, FileText, Shield, Stethoscope } from 'lucide-react';

const Index = () => {
  const [procedures, setProcedures] = useState<Procedure[]>([
    // Sample initial data
    {
      id: "proc_sample_001",
      name: "Sessão de Quimioterapia",
      description: "Administração de medicamentos quimioterápicos para tratamento oncológico",
      category: "Quimioterapia",
      isHighCost: true,
      estimatedDuration: 180,
      createdAt: new Date(Date.now() - 86400000).toISOString(), // Yesterday
      createdBy: "Diretor Médico"
    },
    {
      id: "proc_sample_002",
      name: "Sutura Simples",
      description: "Procedimento básico de sutura para ferimentos superficiais",
      category: "Curativo",
      isHighCost: false,
      estimatedDuration: 30,
      createdAt: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
      createdBy: "Diretor Médico"
    }
  ]);

  const addProcedure = (newProcedure: Procedure) => {
    setProcedures(prev => [newProcedure, ...prev]);
  };

  const highCostCount = procedures.filter(p => p.isHighCost).length;
  const totalProcedures = procedures.length;

  return (
    <div className="min-h-screen bg-gradient-surface">
      {/* Header */}
      <header className="bg-card shadow-card border-b">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-primary flex items-center gap-3">
                <Stethoscope className="h-8 w-8" />
                Sistema Hospitalar - Módulo Procedimentos
              </h1>
              <p className="text-muted-foreground mt-2">
                Gestão e monitoramento de procedimentos médicos com blockchain
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant="outline" className="flex items-center gap-2">
                <FileText className="h-3 w-3" />
                {totalProcedures} tipos cadastrados
              </Badge>
              <Badge 
                variant={highCostCount > 0 ? "destructive" : "secondary"} 
                className="flex items-center gap-2"
              >
                <Shield className="h-3 w-3" />
                {highCostCount} alto custo
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <Tabs defaultValue="monitoring" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-card shadow-card">
            <TabsTrigger value="monitoring" className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Dashboard Tempo Real
            </TabsTrigger>
            <TabsTrigger value="register" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Cadastrar Procedimento
            </TabsTrigger>
            <TabsTrigger value="procedures" className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              Tipos Cadastrados
            </TabsTrigger>
          </TabsList>

          <TabsContent value="monitoring" className="space-y-6">
            <MonitoringDashboard />
          </TabsContent>

          <TabsContent value="register" className="space-y-6">
            <ProcedureTypeForm onProcedureAdded={addProcedure} />
          </TabsContent>

          <TabsContent value="procedures" className="space-y-6">
            <ProcedureTypesList procedures={procedures} />
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="bg-card border-t mt-16">
        <div className="container mx-auto px-6 py-6">
          <div className="text-center text-sm text-muted-foreground">
            <p>Sistema de Gestão Hospitalar - Módulo Procedimentos</p>
            <p className="mt-1">
              Desenvolvido para demonstração de integração blockchain com sistema médico
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
