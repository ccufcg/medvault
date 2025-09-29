import { AlertNotification } from '@/types/medical';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { X, AlertTriangle, User, Wallet, Package, Clock } from 'lucide-react';

interface AlertPopupProps {
  alert: AlertNotification;
  onClose: () => void;
}

export const AlertPopup = ({ alert, onClose }: AlertPopupProps) => {
  const procedure = alert.relatedProcedure;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="max-w-md w-full h-full overflow-y-auto shadow-popup animate-in slide-in-from-bottom-4 duration-300 m-4">
        <CardHeader className="bg-gradient-alert text-white relative rounded-t-lg">
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="absolute right-2 top-2 text-white hover:bg-white/20"
          >
            <X className="h-4 w-4" />
          </Button>
          
          <CardTitle className="flex items-center gap-2 text-white">
            <AlertTriangle className="h-5 w-5" />
            {alert.title}
          </CardTitle>
          <CardDescription className="text-white/90">
            Procedimento de alto custo detectado em tempo real
          </CardDescription>
        </CardHeader>
        
        <CardContent className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <Badge variant="destructive" className="text-sm">
              ALTO CUSTO
            </Badge>
            <span className="text-xs text-muted-foreground">
              {new Date(alert.timestamp).toLocaleString('pt-BR')}
            </span>
          </div>

          {procedure && (
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-foreground mb-2">Detalhes do Procedimento</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Package className="h-4 w-4 text-primary" />
                    <span className="font-medium">{procedure.procedureName}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span>{new Date(procedure.executedAt).toLocaleString('pt-BR')}</span>
                  </div>
                </div>
              </div>

              <Separator />

              <div>
                <h4 className="font-semibold text-foreground mb-2">Profissional Responsável</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-accent" />
                    <span className="font-medium">{procedure.professionalName}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      {procedure.professionalRegistry}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Wallet className="h-4 w-4 text-muted-foreground" />
                    <code className="text-xs bg-muted px-2 py-1 rounded">
                      {procedure.professionalWallet}
                    </code>
                  </div>
                </div>
              </div>

              <Separator />

              <div>
                <h4 className="font-semibold text-foreground mb-2">Paciente</h4>
                <div className="flex items-center gap-2 text-sm">
                  <Wallet className="h-4 w-4 text-muted-foreground" />
                  <code className="text-xs bg-muted px-2 py-1 rounded">
                    {procedure.patientWallet}
                  </code>
                </div>
              </div>

              {procedure.materials && procedure.materials.length > 0 && (
                <>
                  <Separator />
                  <div>
                    <h4 className="font-semibold text-foreground mb-2">Materiais de Alto Custo</h4>
                    <div className="space-y-2">
                      {procedure.materials.map((material, index) => (
                        <div key={index} className="bg-muted/50 p-2 rounded text-sm">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">{material.itemName}</span>
                            <Badge 
                              variant={material.isHighCost ? "destructive" : "secondary"}
                              className="text-xs"
                            >
                              {material.isHighCost ? 'ALTO CUSTO' : 'NORMAL'}
                            </Badge>
                          </div>
                          <div className="text-xs text-muted-foreground mt-1">
                            Lote: {material.lot} | Qtd: {material.quantity}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          <div className="flex gap-2 pt-4">
            <Button
              variant="outline"
              size="sm"
              onClick={onClose}
              className="flex-1"
            >
              Fechar
            </Button>
            <Button
              variant="medical"
              size="sm"
              onClick={() => {
                // In a real system, this would open a detailed view
                console.log("Abrir detalhes do procedimento:", procedure?.id);
                onClose();
              }}
              className="flex-1"
            >
              Ver Detalhes
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};