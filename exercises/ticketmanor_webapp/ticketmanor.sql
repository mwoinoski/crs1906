-- MySQL dump 10.13  Distrib 5.5.11, for Win64 (x86)
--
-- Host: localhost    Database: ticketmanor
-- ------------------------------------------------------
-- Server version	5.5.11

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
-- Table structure for table `acts`
--

DROP TABLE IF EXISTS `acts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acts` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `notes` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acts`
--

LOCK TABLES `acts` WRITE;
/*!40000 ALTER TABLE `acts` DISABLE KEYS */;
INSERT INTO `acts` VALUES (100,NULL,'Star Wars Bloopers',0,2001),(49,NULL,'Bruce Springsteen',NULL,0),(43,NULL,'Bob Sieger',NULL,0),(42,NULL,'Coldplay',NULL,0),(41,NULL,'AC/DC',NULL,0),(39,NULL,'Metallica',NULL,0),(38,NULL,'One Direction',NULL,0),(37,NULL,'Luke Bryan',NULL,0),(36,NULL,'Lana Del Rey',NULL,0),(35,NULL,'Kenny Chesney',NULL,0),(34,NULL,'Houston Rodeo',NULL,0),(33,NULL,'Garth Brooks',NULL,0),(32,NULL,'Foo Fighters',NULL,0),(31,NULL,'Fleetwood Mac',NULL,0),(30,NULL,'Bob Seger',NULL,0),(29,NULL,'Billy Joel',NULL,0),(28,NULL,'Bette Midler',NULL,0),(27,NULL,'Ariana Grande',NULL,0),(26,NULL,'Wynonna Judd',NULL,0),(25,NULL,'U2',NULL,0),(24,NULL,'Toronto Symphony Orchestra',NULL,0),(23,NULL,'The Who',NULL,0),(22,NULL,'The Twinkies',NULL,0),(21,NULL,'The Script',NULL,0),(20,NULL,'The Eagles',NULL,0),(19,NULL,'The Clash',NULL,0),(18,NULL,'Taylor Swift',NULL,0),(17,NULL,'Rod Stewart',NULL,0),(16,NULL,'Neil Diamond',NULL,0),(15,NULL,'Meghan Trainor',NULL,0),(14,NULL,'Maroon 5',NULL,0),(13,NULL,'Los Angeles Philharmonic',NULL,0),(12,NULL,'London Symphony',NULL,0),(11,NULL,'Leonard Cohen',NULL,0),(10,NULL,'Lady Gaga',NULL,0),(9,NULL,'Kenny Chesney',NULL,0),(8,NULL,'Justin Bieber',NULL,0),(7,NULL,'Garth Brooks',NULL,0),(6,NULL,'Foo Fighters',NULL,0),(5,NULL,'Eric Clapton',NULL,0),(4,NULL,'Eddie Money ',NULL,0),(3,NULL,'Boston Pops',NULL,0),(2,NULL,'Beach Boys',NULL,0),(1,NULL,'Rush',NULL,1980),(201,NULL,'Sun Never Sets: The Musical',2,0),(202,NULL,'Nicks vs Raptors',3,0),(203,NULL,'Blue Jays vs Mets',3,0),(204,NULL,'Red Sox vs Maple Leafs',3,0),(205,NULL,'Blackhawks vs Canucks',3,0),(206,NULL,'Real Madrid vs Barcelona',3,0),(52,NULL,'Sun Never Sets: The Musical',2,0),(53,NULL,'Nicks vs Raptors',3,0),(54,NULL,'Blue Jays vs Mets',3,0),(55,NULL,'Red Sox vs Maple Leafs',3,0),(56,NULL,'Blackhawks vs Canucks',3,0),(57,NULL,'Real Madrid vs Barcelona',3,0),(103,NULL,'Sun Never Sets: The Musical',2,0),(104,NULL,'Nicks vs Raptors',3,0),(105,NULL,'Blue Jays vs Mets',3,0),(106,NULL,'Red Sox vs Maple Leafs',3,0),(107,NULL,'Blackhawks vs Canucks',3,0),(108,NULL,'Real Madrid vs Barcelona',3,0),(154,NULL,'Sun Never Sets: The Musical',2,0),(155,NULL,'Nicks vs Raptors',3,0),(156,NULL,'Blue Jays vs Mets',3,0),(157,NULL,'Red Sox vs Maple Leafs',3,0),(158,NULL,'Blackhawks vs Canucks',3,0),(159,NULL,'Real Madrid vs Barcelona',3,0);
/*!40000 ALTER TABLE `acts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acts_events`
--

DROP TABLE IF EXISTS `acts_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acts_events` (
  `acts_id` bigint(20) NOT NULL,
  `events_id` bigint(20) NOT NULL,
  UNIQUE KEY `UK_ckpq2do4le13wa9ww9cjjdprm` (`events_id`),
  KEY `FK_gfkp016vlshfqy1hr15qarmmm` (`acts_id`),
  CONSTRAINT `FK_ckpq2do4le13wa9ww9cjjdprm` FOREIGN KEY (`events_id`) REFERENCES `events` (`id`),
  CONSTRAINT `FK_gfkp016vlshfqy1hr15qarmmm` FOREIGN KEY (`acts_id`) REFERENCES `acts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acts_events`
--

LOCK TABLES `acts_events` WRITE;
/*!40000 ALTER TABLE `acts_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `acts_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_as1rmx4ofyhjguia6ccyf1enx` FOREIGN KEY (`id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditoriums`
--

DROP TABLE IF EXISTS `auditoriums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auditoriums` (
  `id` bigint(20) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `venue_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_liriynofcwhj7asbo25er9tam` (`venue_id`),
  CONSTRAINT `FK_liriynofcwhj7asbo25er9tam` FOREIGN KEY (`venue_id`) REFERENCES `venues` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoriums`
--

LOCK TABLES `auditoriums` WRITE;
/*!40000 ALTER TABLE `auditoriums` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoriums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_customer_id` FOREIGN KEY (`id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `id` bigint(20) NOT NULL,
  `date_time` datetime,
  `venue_id` bigint(20) DEFAULT NULL,
  `what_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_qka83gbjmaflc1ko37xkpojof` (`venue_id`),
  KEY `FK_easseuea032m5cct20tn1dhy5` (`what_id`),
  CONSTRAINT `FK_easseuea032m5cct20tn1dhy5` FOREIGN KEY (`what_id`) REFERENCES `acts` (`id`),
  CONSTRAINT `FK_qka83gbjmaflc1ko37xkpojof` FOREIGN KEY (`venue_id`) REFERENCES `venues` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,NULL,NULL,3),(12,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(13,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',8,3),(14,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(15,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',9,4),(16,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(17,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',10,5),(18,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(19,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',11,6),(20,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(21,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',7,2),(22,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(23,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',8,3),(24,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(25,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',9,4),(26,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(27,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',10,5),(28,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(29,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',11,6),(30,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(31,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',7,2),(32,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(33,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',8,3),(34,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(35,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',9,4),(36,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(37,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',10,5),(38,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0ı·\0x',1,1),(39,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0ı·\0x',11,6),(40,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(41,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',7,2),(42,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(43,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',8,3),(44,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(45,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',9,4),(46,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(47,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',10,5),(48,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(49,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',11,6),(50,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',1,1),(51,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0ı·\0x',7,2),(63,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(64,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',59,54),(65,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(66,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',60,55),(67,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(68,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',61,56),(69,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(70,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',62,57),(71,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(72,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',58,53),(73,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(74,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',59,54),(75,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(76,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',60,55),(77,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(78,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',61,56),(79,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(80,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',62,57),(81,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(82,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',58,53),(83,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(84,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',59,54),(85,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(86,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',60,55),(87,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(88,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',61,56),(89,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0\"°[@x',1,52),(90,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0\"°[@x',62,57),(91,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(92,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',58,53),(93,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(94,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',59,54),(95,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(96,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',60,55),(97,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(98,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',61,56),(99,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(100,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',62,57),(101,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',1,52),(102,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0\"°[@x',58,53),(114,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(115,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',110,105),(116,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(117,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',111,106),(118,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(119,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',112,107),(120,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(121,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',113,108),(122,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(123,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',109,104),(124,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(125,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',110,105),(126,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0	Z¿x',1,103),(127,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\0	Z¿x',111,106),(128,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(129,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',112,107),(130,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(131,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',113,108),(132,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(133,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',109,104),(134,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(135,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',110,105),(136,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(137,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',111,106),(138,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(139,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',112,107),(140,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(141,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',113,108),(142,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\Z\0	Z¿x',1,103),(143,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\Z\0	Z¿x',109,104),(144,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(145,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',110,105),(146,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(147,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',111,106),(148,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(149,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',112,107),(150,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(151,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',113,108),(152,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',1,103),(153,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\0	Z¿x',109,104),(165,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(166,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',161,156),(167,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(168,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',162,157),(169,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(170,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',163,158),(171,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(172,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',164,159),(173,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(174,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',160,155),(175,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(176,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',161,156),(177,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\00;3Äx',1,154),(178,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\n\00;3Äx',162,157),(179,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(180,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',163,158),(181,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(182,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',164,159),(183,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(184,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',160,155),(185,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(186,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',161,156),(187,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(188,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',162,157),(189,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(190,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',163,158),(191,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(192,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',164,159),(193,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\Z\00;3Äx',1,154),(194,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\Z\00;3Äx',160,155),(195,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(196,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',161,156),(197,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(198,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',162,157),(199,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(200,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',163,158),(201,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(202,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',164,159),(203,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',1,154),(204,'¨Ì\0sr\0\rjava.time.Serï]Ñ∫\"H≤\0\0xpw\0\0ﬂ\00;3Äx',160,155);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbackform`
--

DROP TABLE IF EXISTS `feedbackform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedbackform` (
  `id` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `custEmail` varchar(255) DEFAULT NULL,
  `custName` varchar(255) DEFAULT NULL,
  `date` tinyblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbackform`
--

LOCK TABLES `feedbackform` WRITE;
/*!40000 ALTER TABLE `feedbackform` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedbackform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hibernate_sequence`
--

DROP TABLE IF EXISTS `hibernate_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hibernate_sequence` (
  `next_val` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hibernate_sequence`
--

LOCK TABLES `hibernate_sequence` WRITE;
/*!40000 ALTER TABLE `hibernate_sequence` DISABLE KEYS */;
INSERT INTO `hibernate_sequence` VALUES (205);
/*!40000 ALTER TABLE `hibernate_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `members` (
  `profilePhoto` tinyblob,
  `id` bigint(20) NOT NULL,
  `nickName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_15l1eu64rim2shg1s0357e1wn` FOREIGN KEY (`id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (NULL,1,'Mike');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies` (
  `director` varchar(255) DEFAULT NULL,
  `id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_7ia0wlb9huk8qap7q5otg60hm` FOREIGN KEY (`id`) REFERENCES `acts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES ('George Lucas',3);
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_items` (
  `id` bigint(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `sellable_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_dqf6gsmpwc5nn0fdf2sqibl2l` (`sellable_id`),
  CONSTRAINT `FK_dqf6gsmpwc5nn0fdf2sqibl2l` FOREIGN KEY (`sellable_id`) REFERENCES `sellable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `id` bigint(20) NOT NULL,
  `member_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_hk1trr9mwboq35fssa59rnodg` (`member_id`),
  CONSTRAINT `FK_hk1trr9mwboq35fssa59rnodg` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order_items`
--

DROP TABLE IF EXISTS `orders_order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_order_items` (
  `orders_id` bigint(20) NOT NULL,
  `items_id` bigint(20) NOT NULL,
  UNIQUE KEY `UK_trq4mhasmgs7dpi36hk0q8oi4` (`items_id`),
  KEY `FK_3qef3o0ljgieeds6sk3nhcla8` (`orders_id`),
  CONSTRAINT `FK_3qef3o0ljgieeds6sk3nhcla8` FOREIGN KEY (`orders_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `FK_trq4mhasmgs7dpi36hk0q8oi4` FOREIGN KEY (`items_id`) REFERENCES `order_items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order_items`
--

LOCK TABLES `orders_order_items` WRITE;
/*!40000 ALTER TABLE `orders_order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `postcode` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `middles` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES (1,NULL,NULL,NULL,NULL,NULL,NULL,'System','Administrator',NULL);
INSERT INTO `people` VALUES (2,'Springfield','USA','12345','MA','1 Python Place','mike@wxyz.me','Mike','Woinoski',NULL);
INSERT INTO `people` VALUES (3,'Springfield','USA','97478','OR','123 Maple St','marge.simpson@gmail.com','Margret','Simpson','Emily');
INSERT INTO `people` VALUES (4,'Springfield','USA','97478','OR','123 Maple St','homer.simpson@gmail.com','Homer','Simpson','Virgil');
INSERT INTO `people` VALUES (5,'Springfield','USA','97478','OR','125 Maple St','ned.flanders@gmail.com','Ned','Flanders','Abraham');
INSERT INTO `people` VALUES (6,'Chicago','USA','34568','IL','123 Cool St','miles@jazz.com','Miles','Davis','');
/*!40000 ALTER TABLE `people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellable`
--

DROP TABLE IF EXISTS `sellable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sellable` (
  `id` bigint(20) NOT NULL,
  `price` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellable`
--

LOCK TABLES `sellable` WRITE;
/*!40000 ALTER TABLE `sellable` DISABLE KEYS */;
/*!40000 ALTER TABLE `sellable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `price` double DEFAULT NULL,
  `seatNumber` varchar(255) DEFAULT NULL,
  `id` bigint(20) NOT NULL,
  `event_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_meoetyl5jxl895sfugq8l0r96` (`event_id`),
  CONSTRAINT `FK_meoetyl5jxl895sfugq8l0r96` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  CONSTRAINT `FK_ot34u0laq5i3aqxy3qxqkts5e` FOREIGN KEY (`id`) REFERENCES `sellable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venues`
--

DROP TABLE IF EXISTS `venues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venues` (
  `id` bigint(20) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `provState` varchar(255) DEFAULT NULL,
  `streetAddress` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venues`
--

LOCK TABLES `venues` WRITE;
/*!40000 ALTER TABLE `venues` DISABLE KEYS */;
INSERT INTO `venues` VALUES (1,'New York','US',40.764938,-73.979897,'Carnegie Hall','NY','881 Seventh Avenue'),(2,'Toronto','CA',43.646596,-79.386413,'Roy Thompson Hall','ON','60 Simcoe Street'),(7,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(8,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(9,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(10,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(11,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(58,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(59,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(60,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(61,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(62,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(109,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(110,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(111,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(112,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(113,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(160,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(161,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(162,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(163,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(164,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL);
/*!40000 ALTER TABLE `venues` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-01 11:39:45
