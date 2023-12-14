BEGIN;
 -- PROCESO DE CARGA DE LA TABLA SEGURIDAD PERMISOS : sudo -u postgres psql -d dbdesarrollo -a -f /tmp/carga.sql
 -- sudo mv /home/ubuntu/Escritorio/IS2_STAGING/proyecto_CMS/Script/carga.sql /tmp/
-- Insert Roles.
INSERT INTO public."Seguridad_rol"(nombre, descripcion) VALUES
('Administrador', 'Es aquél que puede configurar una página web en su totalidad, crear y publicar contenidos, otorgar permisos a otros usuarios.'),
('Suscriptor', 'Es aquél usuario con una cuenta registrada que tiene la capacidad de interactuar con los contenidos dentro de una página web.'),
('Autor', 'Usuarios que pueden crear sus propios contenidos relacionados a la página. También pueden eliminar comentarios específicos de sus contenidos, inactivar sus contenidos y revisar sus reportes.'),
('Editores', 'Son aquellos usuarios que tienen el permiso de realizar modificaciones en los contenidos que se encuentran en estado de "borrador" o ya publicados.'),
('Publicadores', 'son aquellos usuarios que tienen la capacidad de aprobar o desaprobar la publicación de los contenidos que hayan sido enviados.');

COMMIT;