-- MySQL dump 10.13  Distrib 5.6.43, for Linux (x86_64)
--
-- Host: localhost    Database: sandboxMP
-- ------------------------------------------------------
-- Server version	5.6.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `system_menu`
--

DROP TABLE IF EXISTS `system_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `icon` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `code` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `number` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `system_menu_parent_id_c715739f_fk_system_menu_id` (`parent_id`),
  CONSTRAINT `system_menu_parent_id_c715739f_fk_system_menu_id` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_menu`
--

LOCK TABLES `system_menu` WRITE;
/*!40000 ALTER TABLE `system_menu` DISABLE KEYS */;
INSERT INTO `system_menu` VALUES (1,'系统',NULL,'SYSTEM','/system/',NULL,1),(2,'基础设置','fa fa-gg','SYSTEM-BASIC',NULL,1,1.1),(3,'组织架构',NULL,'SYSTEM-BASIC-STRUCTURE','/system/basic/structure/',2,1.11),(4,'组织架构：列表',NULL,'SYSTEM-BASIC-STRUCTURE-LIST','/system/basic/structure/list/',3,1.111),(5,'组织架构：创建',NULL,'SYSTEM-BASIC-STRUCTURE-CREATE','/system/basic/structure/create/',3,1.112),(6,'组织架构：删除',NULL,'SYSTEM-BASIC-STRUCTURE-DELETE','/system/basic/structure/delete/',3,1.113),(7,'组织架构：关联用户',NULL,'SYSTEM-BASIC-STRUCTURE-ADD_USER','/system/basic/structure/add_user/',3,1.114),(8,'用户管理',NULL,'SYSTEM-BASIC-USER','/system/basic/user/',2,1.12),(9,'用户管理：列表',NULL,'SYSTEM-BASIC-USER-LIST','/system/basic/user/list/',8,1.121),(10,'用户管理：详情',NULL,'SYSTEM-BASIC-USER-DETAIL','/system/basic/user/detail/',8,1.122),(11,'用户管理：修改',NULL,'SYSTEM-BASIC-USER-UPDATE','/system/basic/user/update/',8,1.123),(12,'用户管理：创建',NULL,'SYSTEM-BASIC-USER-CREATE','/system/basic/user/create/',8,1.123),(13,'用户管理：删除',NULL,'SYSTEM-BASIC-USER-DELETE','/system/basic/user/delete/',8,1.124),(14,'用户管理：启用',NULL,'SYSTEM-BASIC-USER-ENABLE','/system/basic/user/enable/',8,1.125),(15,'用户管理：禁用',NULL,'SYSTEM-BASIC-USER-DISABLE','/system/basic/user/disable/',8,1.126),(16,'用户管理：修改密码',NULL,'SYSTEM-BASIC-USER-PASSWORD_CHANGE','/system/basic/user/password_change/',8,1.127),(17,'权限管理','fa fa-user-plus','SYSTEM-RBAC',NULL,1,1.2),(18,'菜单管理',NULL,'SYSTEM-RBAC-MENU','/system/rbac/menu/',17,1.21),(19,'菜单管理：创建',NULL,'SYSTEM-RBAC-MENU-CREATE','/system/rbac/menu/create/',18,1.211),(20,'菜单管理：修改',NULL,'SYSTEM-RBAC-MENU-UPDATE','/system/rbac/menu/update/',18,1.213),(21,'角色管理',NULL,'SYSTEM-RBAC-ROLE','/system/rbac/role/',17,1.22),(22,'角色管理：列表',NULL,'SYSTEM-RBAC-ROLE-LIST','/system/rbac/role/list/',21,1.221),(23,'角色管理：创建',NULL,'SYSTEM-RBAC-ROLE-CREATE','/system/rbac/role/create/',21,1.222),(24,'角色管理：修改',NULL,'SYSTEM-RBAC-ROLE-UPDATE','/system/rbac/role/update/',21,1.223),(25,'角色管理：删除',NULL,'SYSTEM-RBAC-ROLE-DELETE','/system/rbac/role/delete/',21,1.224),(26,'角色管理：关联菜单',NULL,'SYSTEM-RBAC-ROLE-ROLE2MENU','/system/rbac/role/role2menu/',21,1.225),(27,'角色管理：菜单列表',NULL,'SYSTEM-RBAC-ROLE-ROLE2MENU_LIST','/system/rbac/role/role2menu_list/',21,1.226),(28,'角色管理：关联用户',NULL,'SYSTEM-RBAC-ROLE-ROLE2USER','/system/rbac/role/role2user/',21,1.227),(29,'配置管理',NULL,'CMDB','/cmdb/',NULL,2),(30,'平台设置','fa fa-yelp','CMDB-PORTAL',NULL,29,2.1),(31,'字典管理',NULL,'CDMB-PORTAL-CODE','/cmdb/portal/code/',30,2.11),(32,'字典管理：创建',NULL,'CMDB-PORTAL-CODE-CREATE','/cmdb/portal/code/create/',31,2.111),(33,'字典管理：列表',NULL,'CMDB-PORTAL-CODE-LIST','/cmdb/portal/code/list/',31,2.112),(34,'字典管理：修改',NULL,'CMDB-PORTAL-CODE-UPDATE','/cmdb/portal/code/update/',31,2.113),(35,'字典管理：删除',NULL,'CMDB-PORTAL-CODE-DELETE','/cmdb/portal/code/delete/',31,2.114),(36,'扫描配置',NULL,'CMDB-PORTAL-SCAN_CONFIG','/cmdb/portal/scan_config/',30,2.12),(37,'设备扫描',NULL,'CDMB-PORTAL-DEVICE_SCAN','/cmdb/portal/device_scan/',30,2.13),(38,'设备扫描：执行',NULL,'CMDB-PORTAL-DEVICE_SCAN-EXEC','/cmdb/portal/device_scan/exec/',37,2.131),(39,'设备扫描：列表',NULL,'CMDB-PORTAL-DEVICE_SCAN-LIST','/cmdb/portal/device_scan/list/',37,2.132),(40,'设备扫描：详情',NULL,'CMDB-PORTAL/DEVICE_SCAN/DETAIL','/cmdb/portal/device_scan/detail/',37,2.133),(41,'设备扫描：删除',NULL,'CMDB-PORTAL-DEVICE-_SCAN-DELETE','/cmdb/portal/device_scan/delete/',37,2.134),(42,'资产管理','fa fa-desktop','CMDB-EAM',NULL,29,2.2),(43,'机柜管理',NULL,'CMDB-EAM-CABINET','/cmdb/eam/cabinet/',42,2.21),(44,'机柜管理：新增',NULL,'CMDB-EAM-CABINET-CREATE','/cmdb/eam/cabinet/create/',43,2.211),(45,'机柜管理：修改',NULL,'CMDB-EAM-CABINET-UPDATE','/cmdb/eam/cabinet/update/',43,2.212),(46,'机柜管理：列表',NULL,'CMDB-EAM-CABINET-LIST','/cmdb/eam/cabinet/list/',43,2.213),(47,'机柜管理：删除',NULL,'CMDB-EAM-CABINET-DELETE','/cmdb/eam/cabinet/delete/',43,2.214),(48,'设备管理',NULL,'CMDB-EAM-DEVICE','/cmdb/eam/device/',42,2.22),(49,'设备管理：列表',NULL,'CMDB-EAM-DEVICE-LIST','/cmdb/eam/device/list/',48,2.221),(50,'设备管理：新增',NULL,'CMDB-EAM-DEVICE-CREATE','/cmdb/eam/device/create/',48,2.222),(51,'设备管理：修改',NULL,'CMDB-EAM-DEVICE-UPDATE','/cmdb/eam/device/update/',48,2.223),(52,'设备扫描：入库',NULL,'CMDB-PORTAL-DEVICE_SCAN-INBOUND','/cmdb/portal/device_scan/inbound/',37,2.135),(53,'设备管理：认证管理',NULL,'CMDB-EAM-DEVICE-DEVICE2CONNECTION','/cmdb/eam/device/device2connection/',48,2.224),(54,'设备管理：删除',NULL,'CMDB-EAM-DEVICE-DELETE','/cmdb/eam/device/delete/',37,2.225),(55,'设备管理：详情',NULL,'CMDB-EAM-DEVICE-DETAIL','/cmdb/eam/device/detail/',48,2.226),(56,'设备管理：上传',NULL,'CMDB-EAM-DEVICE-UPLOAD','/cmdb/eam/device/upload/',48,2.227),(57,'设备管理：删除文件',NULL,'CMDB-EAM-DEVICE-FILE_DELETE','/cmdb/eam/device/file_delete/',48,2.228),(58,'设备管理：自动更新',NULL,'CMDB-EAM-DEVICE-AUTO_UPDATE_DEVICE_INFO','/cmdb/eam/device/auto_update_device_info/',48,2.229);
/*!40000 ALTER TABLE `system_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_role`
--

DROP TABLE IF EXISTS `system_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `desc` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role`
--

LOCK TABLES `system_role` WRITE;
/*!40000 ALTER TABLE `system_role` DISABLE KEYS */;
INSERT INTO `system_role` VALUES (1,'管理员组','系统默认角色组，具有系统管理的全部权限');
/*!40000 ALTER TABLE `system_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_userprofile`
--

DROP TABLE IF EXISTS `system_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `mobile` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `post` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `superior_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `system_userprofile_department_id_a46d57f9_fk_system_structure_id` (`department_id`),
  KEY `system_userprofile_superior_id_6b0fd92f_fk_system_userprofile_id` (`superior_id`),
  CONSTRAINT `system_userprofile_department_id_a46d57f9_fk_system_structure_id` FOREIGN KEY (`department_id`) REFERENCES `system_structure` (`id`),
  CONSTRAINT `system_userprofile_superior_id_6b0fd92f_fk_system_userprofile_id` FOREIGN KEY (`superior_id`) REFERENCES `system_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_userprofile`
--

LOCK TABLES `system_userprofile` WRITE;
/*!40000 ALTER TABLE `system_userprofile` DISABLE KEYS */;
INSERT INTO `system_userprofile` VALUES (1,'pbkdf2_sha256$120000$qFLcOe8f3gr9$UrT1tFbDnFUaoqV5jZ9F5Xx9duYy33ZVZPauTb20xTU=','2019-02-17 21:18:45.791223',1,'admin','','',1,1,'2019-01-31 00:12:32.113271','管理员',NULL,'male','13951994649','robbie_han@outlook.com','image/default.jpg',NULL,NULL,NULL);
/*!40000 ALTER TABLE `system_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_userprofile_roles`
--

DROP TABLE IF EXISTS `system_userprofile_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_userprofile_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userprofile_roles_userprofile_id_role_id_459e3bc3_uniq` (`userprofile_id`,`role_id`),
  KEY `system_userprofile_roles_role_id_cc2781b0_fk_system_role_id` (`role_id`),
  CONSTRAINT `system_userprofile_r_userprofile_id_0247f4f3_fk_system_us` FOREIGN KEY (`userprofile_id`) REFERENCES `system_userprofile` (`id`),
  CONSTRAINT `system_userprofile_roles_role_id_cc2781b0_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_userprofile_roles`
--

LOCK TABLES `system_userprofile_roles` WRITE;
/*!40000 ALTER TABLE `system_userprofile_roles` DISABLE KEYS */;
INSERT INTO `system_userprofile_roles` VALUES (1,1,1);
/*!40000 ALTER TABLE `system_userprofile_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_role_permissions`
--

DROP TABLE IF EXISTS `system_role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_role_permissions_role_id_menu_id_91fb438a_uniq` (`role_id`,`menu_id`),
  KEY `system_role_permissions_menu_id_f48d14c7_fk_system_menu_id` (`menu_id`),
  CONSTRAINT `system_role_permissions_menu_id_f48d14c7_fk_system_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_role_permissions_role_id_a52abc64_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role_permissions`
--

LOCK TABLES `system_role_permissions` WRITE;
/*!40000 ALTER TABLE `system_role_permissions` DISABLE KEYS */;
INSERT INTO `system_role_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,1,41),(44,1,42),(45,1,43),(46,1,44),(47,1,45),(48,1,46),(49,1,47),(50,1,48),(51,1,49),(52,1,50),(53,1,51),(42,1,52),(54,1,53),(43,1,54),(55,1,55),(56,1,56),(57,1,57),(58,1,58);
/*!40000 ALTER TABLE `system_role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_code`
--

DROP TABLE IF EXISTS `cmdb_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `desc` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_code_parent_id_21a5a774_fk_cmdb_code_id` (`parent_id`),
  CONSTRAINT `cmdb_code_parent_id_21a5a774_fk_cmdb_code_id` FOREIGN KEY (`parent_id`) REFERENCES `cmdb_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_code`
--

LOCK TABLES `cmdb_code` WRITE;
/*!40000 ALTER TABLE `cmdb_code` DISABLE KEYS */;
INSERT INTO `cmdb_code` VALUES (1,'NETWORK_TYPE','网络类型','网络类型',NULL),(2,'SERVICE_TYPE','服务类型','0',NULL),(3,'OPERATION_TYPE','业务类型','0',NULL),(4,'NETWORK_TYPE_PRD','生产网','0',1),(5,'NETWORK_TYPE_PRE','预发布网','0',1),(6,'NETWORK_TYPE_TEST','测试网','0',1),(7,'NETWORK_TYPE_DEV','办公网','0',1),(8,'NETWORK_TYPE_MANAGE','管理网','0',1),(9,'SERVICE_TYPE_PROXY','代理服务','0',2),(10,'SERVICE_TYPE_APPSERVICE','TOMCAT服务','0',2),(11,'SERVICE_TYPE_MYSQL','MYSQL服务','0',2),(12,'SERVICE_TYPE_MONGODB','MONGODB服务','0',2),(13,'SERVICE_TYPE_REDIS','REDIS服务','0',2),(14,'SERVICE_TYPE_FILE','文件服务','0',2),(15,'SERVICE_TYPE_MQ','MQ服务','0',2),(16,'SERVICE_TYPE_MEMCACHED','MEMCACHED服务','0',2),(17,'SYSTEM_TYPE_MAIL','邮件系统','0',3),(18,'SYSTEM_TYPE_IM','即时通信讯','0',3);
/*!40000 ALTER TABLE `cmdb_code` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-25 19:37:59
