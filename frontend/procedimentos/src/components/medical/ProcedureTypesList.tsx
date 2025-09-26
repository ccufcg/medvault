import { Procedure } from '@/types/medical';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Clock, AlertTriangle, CheckCircle } from 'lucide-react';

interface ProcedureTypesListProps {
  procedures: Procedure[];
}

export const ProcedureTypesList = ({ procedures }: ProcedureTypesListProps) => {
  const getCategoryIcon = (category: Procedure['category']) => {
    const icons = {
      'Cirurgia': '🔧',
      'Consulta': '👨‍⚕️',
      'Exame': '🔬',
      'Curativo': '🩹',
      'Quimioterapia': '💊',
      'Outros': '📋'
    };
    return icons[category] || '📋';
  };

  const getCategoryColor = (category: Procedure['category']) => {
    const colors = {
      'Cirurgia': 'bg-error/10 text-error border-error/20',
      'Consulta': 'bg-primary/10 text-primary border-primary/20',
      'Exame': 'bg-accent/10 text-accent border-accent/20',
      'Curativo': 'bg-warning/10 text-warning border-warning/20',
      'Quimioterapia': 'bg-critical/10 text-critical border-critical/20',
      'Outros': 'bg-muted text-muted-foreground border-muted'
    };
    return colors[category] || colors['Outros'];
  };

  if (procedures.length === 0) {
    return (
      <Card className="shadow-card">
        <CardContent className="p-8 text-center">
          <FileText className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
          <p className="text-muted-foreground mb-2">Nenhum tipo de procedimento cadastrado</p>
          <p className="text-sm text-muted-foreground">
            Use o formulário acima para registrar novos tipos de procedimentos
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-foreground">
          <FileText className="h-5 w-5" />
          Tipos de Procedimentos Cadastrados ({procedures.length})
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {procedures.map((procedure) => (
            <div
              key={procedure.id}
              className="border rounded-lg p-4 hover:shadow-md transition-all duration-300 bg-card hover:bg-accent/5"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-lg">
                    {getCategoryIcon(procedure.category)}
                  </span>
                  <h3 className="font-semibold text-sm line-clamp-2">
                    {procedure.name}
                  </h3>
                </div>
                
                {procedure.isHighCost && (
                  <AlertTriangle className="h-4 w-4 text-warning flex-shrink-0" />
                )}
              </div>

              <div className="space-y-2">
                <Badge 
                  className={`text-xs ${getCategoryColor(procedure.category)} border`}
                >
                  {procedure.category}
                </Badge>

                {procedure.description && (
                  <p className="text-xs text-muted-foreground line-clamp-2">
                    {procedure.description}
                  </p>
                )}

                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {procedure.estimatedDuration}min
                  </div>
                  
                  {procedure.isHighCost ? (
                    <Badge variant="destructive" className="text-xs">
                      Alto Custo
                    </Badge>
                  ) : (
                    <div className="flex items-center gap-1 text-success">
                      <CheckCircle className="h-3 w-3" />
                      <span>Normal</span>
                    </div>
                  )}
                </div>

                <div className="text-xs text-muted-foreground pt-1 border-t">
                  Criado em {new Date(procedure.createdAt).toLocaleDateString('pt-BR')}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};