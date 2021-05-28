-- Documentation https://mariadb.com/kb/en/sql-statements/

CREATE DATABASE IF NOT EXISTS OurData
    CHARACTER SET = "utf8mb4"
;

CREATE USER 'adminman'@'%' IDENTIFIED BY "hi!";

-- show users
SELECT host, user, password FROM mysql.user;
-- Cambiar en el archivo ,config.inc.php,   dentro de E:\xampp\phpMyAdmin  (in my case)
-- in the end, for http, refresh, then for cookie, and refresh, '$cfg['Servers'][$i]['auth_type'] = 'cookie';

GRANT ALL PRIVILEGES 
  ON OurData.*
  TO 'adminman'@'%';