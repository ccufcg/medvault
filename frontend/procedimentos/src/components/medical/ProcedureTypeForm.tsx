import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Procedure } from '@/types/medical';
import { useToast } from '@/hooks/use-toast';
import { Plus, FileText, Clock, AlertTriangle } from 'lucide-react';

interface ProcedureTypeFormProps {
  onProcedureAdded: (procedure: Procedure) => void;
}

export const ProcedureTypeForm = ({ onProcedureAdded }: ProcedureTypeFormProps) => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '' as Procedure['category'],
    isHighCost: false,
    estimatedDuration: 30
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newProcedure: Procedure = {
        id: `proc_type_${Date.now()}`,
        ...formData,
        category: formData.category as Procedure['category'],
        createdAt: new Date().toISOString(),
        createdBy: "Diretor Médico" // Mock user
      };

      onProcedureAdded(newProcedure);
      
      toast({
        title: "✅ Tipo de Procedimento Cadastrado",
        description: `${newProcedure.name} foi registrado no sistema com sucesso.`,
        variant: "default"
      });

      // Reset form
      setFormData({
        name: '',
        description: '',
        category: '' as Procedure['category'],
        isHighCost: false,
        estimatedDuration: 30
      });

    } catch (error) {
      toast({
        title: "❌ Erro no Cadastro",
        description: "Não foi possível cadastrar o procedimento. Tente novamente.",
        variant: "destructive"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="shadow-card bg-gradient-surface">
      <CardHeader className="bg-card-header">
        <CardTitle className="flex items-center gap-2 text-primary">
          <FileText className="h-5 w-5" />
          Cadastro de Tipos de Procedimento
        </CardTitle>
        <CardDescription>
          Registre novos tipos de procedimentos médicos no sistema blockchain
        </CardDescription>
      </CardHeader>
      <CardContent className="p-6 space-y-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name" className="font-medium text-foreground">
                Nome do Procedimento *
              </Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="ex: Sessão de Quimioterapia"
                required
                className="transition-medical"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="category" className="font-medium text-foreground">
                Categoria *
              </Label>
              <Select 
                value={formData.category} 
                onValueChange={(value) => setFormData(prev => ({ ...prev, category: value as Procedure['category'] }))}
              >
                <SelectTrigger className="transition-medical">
                  <SelectValue placeholder="Selecione a categoria" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Cirurgia">🔧 Cirurgia</SelectItem>
                  <SelectItem value="Consulta">👨‍⚕️ Consulta</SelectItem>
                  <SelectItem value="Exame">🔬 Exame</SelectItem>
                  <SelectItem value="Curativo">🩹 Curativo</SelectItem>
                  <SelectItem value="Quimioterapia">💊 Quimioterapia</SelectItem>
                  <SelectItem value="Outros">📋 Outros</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="font-medium text-foreground">
              Descrição do Procedimento
            </Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Descreva detalhadamente o procedimento..."
              rows={3}
              className="transition-medical"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="duration" className="font-medium text-foreground flex items-center gap-2">
                <Clock className="h-4 w-4" />
                Duração Estimada (minutos)
              </Label>
              <Input
                id="duration"
                type="number"
                min="1"
                max="480"
                value={formData.estimatedDuration}
                onChange={(e) => setFormData(prev => ({ ...prev, estimatedDuration: parseInt(e.target.value) || 30 }))}
                className="transition-medical"
              />
            </div>

            <div className="space-y-3">
              <Label className="font-medium text-foreground flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-warning" />
                Procedimento de Alto Custo
              </Label>
              <div className="flex items-center space-x-3">
                <Switch
                  checked={formData.isHighCost}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, isHighCost: checked }))}
                />
                <span className="text-sm text-muted-foreground">
                  {formData.isHighCost ? 'Materiais de alto custo serão monitorados' : 'Procedimento padrão'}
                </span>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <Button
              type="submit"
              variant="medical"
              size="lg"
              disabled={isSubmitting || !formData.name || !formData.category}
              className="min-w-[200px]"
            >
              {isSubmitting ? (
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Registrando...
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Cadastrar Procedimento
                </div>
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};