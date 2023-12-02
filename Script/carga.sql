BEGIN;

 -- PROCESO DE CARGA DE LA TABLA SEGURIDAD PERMISOS : sudo -u postgres psql -d dbdesarrollo -a -f /tmp/carga.sql
 -- sudo mv /home/ubuntu/Escritorio/IS2_STAGING/proyecto_CMS/Script/carga.sql /tmp/
INSERT INTO public."Seguridad_permiso" (nombre, descripcion) VALUES 
('ECU-001-Inicio del sistema', 'Permite al usuario iniciar el sistema'),
('ECU-002-Iniciar sesión', 'Permite al usuario iniciar sesión en el sistema'),
('ECU-003-Cerrar Sesión', 'Permite al usuario cerrar sesión en el sistema'),
('ECU-004-Listar Usuarios', 'Permite al usuario listar todos los usuarios del sistema'),
('ECU-005-Dar acceso a Usuario', 'Permite otorgar acceso a un usuario'),
('ECU-006-Dar de Baja Usuario', 'Permite dar de baja a un usuario del sistema'),
('ECU-007-Crear Rol', 'Permite crear un nuevo rol de usuario'),
('ECU-008-Modificar Rol', 'Permite modificar un rol de usuario existente'),
('ECU-009-Eliminar Rol', 'Permite eliminar un rol de usuario'),
('ECU-010-Asignar Rol', 'Permite asignar un rol a un usuario'),
('ECU-011-Desasignar Rol a un Usuario', 'Permite desasignar un rol de un usuario'),
('ECU-012-Listar Roles', 'Permite listar todos los roles disponibles en el sistema'),
('ECU-013-Crear Permiso', 'Permite crear un nuevo permiso'),
('ECU-014-Asignar Permiso', 'Permite asignar un permiso a un rol'),
('ECU-015-Listar Permisos', 'Permite listar todos los permisos disponibles en el sistema'),
('ECU-016-Listar plantillas', 'Permite listar todas las plantillas disponibles'),
('ECU-017-Seleccionar plantilla', 'Permite seleccionar una plantilla para uso'),
('ECU-018-Crear tipos de contenido', 'Permite crear nuevos tipos de contenido'),
('ECU-019-Listar tipos de contenido', 'Permite listar los tipos de contenido disponibles'),
('ECU-020-Crear contenido', 'Permite crear nuevo contenido'),
('ECU-021-Editar contenido', 'Permite editar contenido existente'),
('ECU-022-Modificar estado de un Contenido', 'Permite cambiar el estado de un contenido'),
('ECU-023-Listar contenidos', 'Permite listar todos los contenidos'),
('ECU-024-Crear categoría', 'Permite crear una nueva categoría'),
('ECU-025-Modificar categoría', 'Permite modificar una categoría existente'),
('ECU-026-Modificar estado de una categoría', 'Permite cambiar el estado de una categoría'),
('ECU-027-Listar categorías', 'Permite listar todas las categorías existentes'),
('ECU-028-Suscribirse a una categoría', 'Permite a un usuario suscribirse a una categoría para recibir actualizaciones'),
('ECU-029-Crear subcategoría', 'Permite crear una nueva subcategoría dentro de una categoría existente'),
('ECU-030-Asociar subcategoría a una categoría', 'Permite asociar una subcategoría existente con una categoría'),
('ECU-031-Modificar subcategoría', 'Permite modificar una subcategoría existente'),
('ECU-032-Listar subcategorías', 'Permite listar todas las subcategorías existentes'),
('ECU-033-Mostrar notificaciones al usuario', 'Permite mostrar notificaciones al usuario'),
('ECU-034-Mostrar reportes estadísticos del Sistema', 'Permite mostrar reportes estadísticos del sistema'),
('ECU-035-Visualizar Tablero Kanban', 'Permite visualizar el tablero Kanban de proyectos');

COMMIT;
