from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django_enumfield import enum


class State(enum.Enum):
  """
  Usada para representar los estados de los registros.
  """

  ACTIVE = 1
  INACTIVE = 2

  labels = {
    ACTIVE: 'activo',
    INACTIVE: 'inactivo'
  }


class SoftDeletionQuerySet(QuerySet):
  """
  Clase SoftDeletionQuerySet sobrescribe el metodo delete para evitar eliminar
  un registro y cambiar el estado.
  """

  def delete(self, deleted_by):
    """
    Cambia el estado de un registro a Inactivo.
    :param deleted_by:User
    :return: QuerySet
    """

    return super(SoftDeletionQuerySet, self).update(
      deleted_date=timezone.now(),
      state=State.INACTIVE,
      deleted_by=deleted_by)

  def hard_delete(self):
    """
    Elimina un usando el metodo delete.
    :return: QuerySet
    """

    return super(SoftDeletionQuerySet, self).delete()


class SoftDeletionManager(models.Manager):
  """
  Clase SoftDeletionManager usada para manejar las actualizaciones de los
  usuarios.
  """

  def __init__(self, *args, **kwargs):
    """
    Constructor de la clase. Inicializa con el parametro alive_only con el
    parametro True para asegurar que solo obtiene los objetos de estado activo
    y sin fecha de eliminacion.
    :param args:
    :param kwargs:
    """

    self.alive_only = kwargs.pop('alive_only', True)
    super(SoftDeletionManager, self).__init__(*args, **kwargs)

  def get_queryset(self):
    """
    Retorna los objetos activos y sin fecha de eliminacion cuando el atributo
    alive_only esta activo.
    :return: QuerySet
    """

    if self.alive_only:
      return SoftDeletionQuerySet(self.model).filter(state=State.ACTIVE,
                                                     deleted_date=None)
    return SoftDeletionQuerySet(self.model)

  def hard_delete(self):
    """
    Crea el metodo hard_delete para un QuerySet.
    :return: QuerySet
    """

    return self.get_queryset().hard_delete()


class Auditor(models.Model):
  """
  Clase abstracta para generar auditorias sobre los modelos.
  """

  created_date = models.DateTimeField(auto_now_add=True,
                                      help_text='Fecha de creacion')
  created_by = models.ForeignKey(User,
                                 related_name='%(class)s_created_by',
                                 help_text='Usuario que crea el objeto',
                                 on_delete=models.CASCADE)
  updated_date = models.DateTimeField(null=True,
                                      auto_now=True,
                                      help_text='Fecha de actualizacion')
  updated_by = models.ForeignKey(User,
                                 null=True,
                                 related_name='%(class)s_updated_by',
                                 help_text='Usuario que actualiza el objeto',
                                 on_delete=models.CASCADE)
  deleted_date = models.DateTimeField(null=True,
                                      help_text='Fecha de eliminacion')
  deleted_by = models.ForeignKey(User,
                                 null=True,
                                 related_name='%(class)s_deleted_by',
                                 help_text='Usuario que elimina el objeto',
                                 on_delete=models.CASCADE)
  state = enum.EnumField(State, default=State.ACTIVE)

  objects = SoftDeletionManager()
  all_objects = SoftDeletionManager(alive_only=False)

  class Meta:
    abstract = True

  def delete(self, deleted_by, using=None):
    """
    Sobrescribe el metodo delete para evitar eliminar el registro
    :param deleted_by:User
    :param using:str
    :return: None
    """

    self.deleted_by = deleted_by
    self.state = State.INACTIVE
    self.deleted_date = timezone.now()
    self.save(using=using)

  def hard_delete(self, using=None):
    """
    Usado para eliminar el registro.
    :param using:str
    :return: Auditor
    """

    super(Auditor, self).delete(using=using)
