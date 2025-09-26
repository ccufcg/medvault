import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { blockchainService } from '@/services/mockBlockchain';
import { BlockchainEvent, AlertNotification } from '@/types/medical';
import { AlertPopup } from './AlertPopup';
import { Activity, Shield, Zap, Eye, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

export const MonitoringDashboard = () => {
  const [isListening, setIsListening] = useState(false);
  const [alerts, setAlerts] = useState<AlertNotification[]>([]);
  const [recentEvents, setRecentEvents] = useState<BlockchainEvent[]>([]);
  const [currentAlert, setCurrentAlert] = useState<AlertNotification | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const unsubscribe = blockchainService.subscribe(handleBlockchainEvent);
    return unsubscribe;
  }, []);

  const handleBlockchainEvent = (event: BlockchainEvent) => {
    console.log("📡 Dashboard recebeu evento:", event);
    
    setRecentEvents(prev => [event, ...prev.slice(0, 9)]);

    if (event.type === 'HIGH_COST_MATERIAL_USED') {
      const alert: AlertNotification = {
        id: `alert_${Date.now()}`,
        type: 'HIGH_COST_PROCEDURE',
        title: '🚨 Material de Alto Custo Detectado',
        message: `Procedimento: ${event.data.procedureName} utilizando materiais de alto custo.`,
        timestamp: event.timestamp,
        isRead: false,
        severity: 'high',
        relatedProcedure: {
          id: event.data.procedureId,
          procedureId: event.data.procedureId,
          procedureName: event.data.procedureName,
          procedureType: event.data.procedureName,
          patientWallet: event.data.patientWallet,
          professionalWallet: event.data.professionalWallet,
          professionalName: event.data.professionalName,
          professionalRegistry: event.data.professionalRegistry,
          executedAt: event.data.timestamp,
          materials: event.data.materials,
          isHighCostMaterials: true,
          status: 'Em Andamento'
        }
      };

      setAlerts(prev => [alert, ...prev]);
      setCurrentAlert(alert);

      toast({
        title: "🚨 Alerta de Alto Custo",
        description: `${event.data.professionalName} está utilizando materiais de alto custo`,
        variant: "destructive"
      });
    }
  };

  const startMonitoring = () => {
    blockchainService.startListening();
    setIsListening(true);
    toast({
      title: "🔗 Monitoramento Ativo",
      description: "Sistema conectado à blockchain - Escutando eventos em tempo real",
      variant: "default"
    });
  };

  const stopMonitoring = () => {
    blockchainService.stopListening();
    setIsListening(false);
    toast({
      title: "📴 Monitoramento Pausado",
      description: "Conexão com blockchain interrompida",
      variant: "default"
    });
  };

  const simulateHighCostEvent = () => {
    blockchainService.simulateHighCostProcedure();
    toast({
      title: "🧪 Evento Simulado",
      description: "Procedimento de alto custo simulado para demonstração",
      variant: "default"
    });
  };

  const markAlertAsRead = (alertId: string) => {
    setAlerts(prev => 
      prev.map(alert => 
        alert.id === alertId ? { ...alert, isRead: true } : alert
      )
    );
  };

  const closeCurrentAlert = () => {
    if (currentAlert) {
      markAlertAsRead(currentAlert.id);
      setCurrentAlert(null);
    }
  };

  const getEventIcon = (type: BlockchainEvent['type']) => {
    switch (type) {
      case 'HIGH_COST_MATERIAL_USED':
        return <AlertTriangle className="h-4 w-4 text-critical" />;
      case 'PROCEDURE_REGISTERED':
        return <Activity className="h-4 w-4 text-primary" />;
      case 'PROCEDURE_COMPLETED':
        return <CheckCircle className="h-4 w-4 text-success" />;
      default:
        return <Clock className="h-4 w-4 text-muted-foreground" />;
    }
  };

  const getEventBadgeVariant = (type: BlockchainEvent['type']) => {
    switch (type) {
      case 'HIGH_COST_MATERIAL_USED':
        return 'destructive';
      case 'PROCEDURE_REGISTERED':
        return 'default';
      case 'PROCEDURE_COMPLETED':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-medical bg-gradient-surface">
        <CardHeader className="bg-card-header">
          <CardTitle className="flex items-center gap-2 text-primary">
            <Shield className="h-5 w-5" />
            Dashboard de Monitoramento - Módulo Procedimentos
          </CardTitle>
          <CardDescription>
            Monitoramento em tempo real de eventos blockchain e alertas de alto custo
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${isListening ? 'bg-success animate-pulse' : 'bg-muted'}`}></div>
                <span className="font-medium">
                  Status: {isListening ? 'Conectado' : 'Desconectado'}
                </span>
              </div>
              
              <Badge variant={isListening ? 'default' : 'secondary'} className="flex items-center gap-1">
                <Eye className="h-3 w-3" />
                {recentEvents.length} eventos recentes
              </Badge>
              
              <Badge variant="outline" className="flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                {alerts.filter(a => !a.isRead).length} alertas não lidos
              </Badge>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={simulateHighCostEvent}
                className="transition-medical"
              >
                <Zap className="h-4 w-4 mr-1" />
                Simular Evento
              </Button>
              
              {isListening ? (
                <Button
                  variant="destructive"
                  onClick={stopMonitoring}
                  className="transition-medical"
                >
                  📴 Pausar Monitoramento
                </Button>
              ) : (
                <Button
                  variant="medical"
                  onClick={startMonitoring}
                  className="transition-medical"
                >
                  🔗 Iniciar Monitoramento
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-foreground">
              <Activity className="h-5 w-5" />
              Eventos Recentes da Blockchain
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4">
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {recentEvents.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>Nenhum evento detectado ainda</p>
                  <p className="text-sm">Inicie o monitoramento para ver eventos</p>
                </div>
              ) : (
                recentEvents.map((event) => (
                  <div
                    key={event.id}
                    className="flex items-start gap-3 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
                  >
                    {getEventIcon(event.type)}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant={getEventBadgeVariant(event.type)} className="text-xs">
                          {event.type.replace(/_/g, ' ')}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          Block #{event.blockNumber}
                        </span>
                      </div>
                      <p className="text-sm font-medium truncate">
                        {event.data.procedureName || 'Evento da blockchain'}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(event.timestamp).toLocaleString('pt-BR')}
                      </p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-foreground">
              <AlertTriangle className="h-5 w-5" />
              Alertas do Sistema
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4">
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {alerts.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Shield className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>Nenhum alerta registrado</p>
                  <p className="text-sm">Sistema funcionando normalmente</p>
                </div>
              ) : (
                alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className={`p-3 rounded-lg border transition-colors cursor-pointer hover:bg-accent/50 ${
                      !alert.isRead ? 'bg-critical/5 border-critical/20' : 'bg-card'
                    }`}
                    onClick={() => markAlertAsRead(alert.id)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <Badge 
                        variant={alert.severity === 'high' ? 'destructive' : 'secondary'}
                        className="text-xs"
                      >
                        {alert.severity.toUpperCase()}
                      </Badge>
                      {!alert.isRead && (
                        <div className="w-2 h-2 rounded-full bg-critical"></div>
                      )}
                    </div>
                    <p className="text-sm font-medium">{alert.title}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(alert.timestamp).toLocaleString('pt-BR')}
                    </p>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {currentAlert && (
        <AlertPopup
          alert={currentAlert}
          onClose={closeCurrentAlert}
        />
      )}
    </div>
  );
};