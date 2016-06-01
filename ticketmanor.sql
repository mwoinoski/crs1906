-- MySQL dump 10.13  Distrib 5.7.7-rc, for Win64 (x86_64)
--
-- Host: localhost    Database: ticketmanor
-- ------------------------------------------------------
-- Server version	5.7.7-rc-log

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
) ENGINE=InnoDB AUTO_INCREMENT=306 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acts`
--

LOCK TABLES `acts` WRITE;
/*!40000 ALTER TABLE `acts` DISABLE KEYS */;
INSERT INTO `acts` VALUES (1,NULL,'Rush',1,1980),(2,NULL,'Beach Boys',1,0),(3,NULL,'Boston Pops',1,0),(4,NULL,'Eddie Money ',1,0),(5,NULL,'Eric Clapton',1,0),(6,NULL,'Foo Fighters',1,0),(7,NULL,'Garth Brooks',1,0),(8,NULL,'Justin Bieber',1,0),(9,NULL,'Kenny Chesney',1,0),(10,NULL,'Lady Gaga',1,0),(11,NULL,'Leonard Cohen',1,0),(12,NULL,'London Symphony',1,0),(13,NULL,'Los Angeles Philharmonic',1,0),(14,NULL,'Maroon 5',1,0),(15,NULL,'Meghan Trainor',1,0),(16,NULL,'Neil Diamond',1,0),(17,NULL,'Rod Stewart',1,0),(18,NULL,'Taylor Swift',1,0),(19,NULL,'The Clash',1,0),(20,NULL,'The Eagles',1,0),(21,NULL,'The Script',1,0),(22,NULL,'The Twinkies',1,0),(23,NULL,'The Who',1,0),(24,NULL,'Toronto Symphony Orchestra',1,0),(25,NULL,'U2',1,0),(26,NULL,'Wynonna Judd',1,0),(27,NULL,'Ariana Grande',1,0),(28,NULL,'Bette Midler',1,0),(29,NULL,'Billy Joel',1,0),(30,NULL,'Bob Seger',1,0),(31,NULL,'Fleetwood Mac',1,0),(32,NULL,'Foo Fighters',1,0),(33,NULL,'Garth Brooks',1,0),(34,NULL,'Houston Rodeo',1,0),(35,NULL,'Kenny Chesney',1,0),(36,NULL,'Lana Del Rey',1,0),(37,NULL,'Luke Bryan',1,0),(38,NULL,'One Direction',1,0),(39,NULL,'Metallica',1,0),(41,NULL,'AC/DC',1,0),(42,NULL,'Coldplay',1,0),(43,NULL,'Bob Sieger',1,0),(49,NULL,'Bruce Springsteen',1,0),(52,NULL,'Sun Never Sets: The Musical',2,0),(53,NULL,'Nicks vs Raptors',3,0),(54,NULL,'Blue Jays vs Mets',3,0),(55,NULL,'Red Sox vs Maple Leafs',3,0),(56,NULL,'Blackhawks vs Canucks',3,0),(57,NULL,'Real Madrid vs Barcelona',3,0),(100,NULL,'Star Wars Bloopers',0,2001),(103,NULL,'Sun Never Sets: The Musical',2,0),(104,NULL,'Nicks vs Raptors',3,0),(105,NULL,'Blue Jays vs Mets',3,0),(106,NULL,'Red Sox vs Maple Leafs',3,0),(107,NULL,'Blackhawks vs Canucks',3,0),(108,NULL,'Real Madrid vs Barcelona',3,0),(154,NULL,'Sun Never Sets: The Musical',2,0),(155,NULL,'Nicks vs Raptors',3,0),(156,NULL,'Blue Jays vs Mets',3,0),(157,NULL,'Red Sox vs Maple Leafs',3,0),(158,NULL,'Blackhawks vs Canucks',3,0),(159,NULL,'Real Madrid vs Barcelona',3,0),(201,NULL,'Sun Never Sets: The Musical',2,0),(202,NULL,'Nicks vs Raptors',3,0),(203,NULL,'Blue Jays vs Mets',3,0),(204,NULL,'Red Sox vs Maple Leafs',3,0),(205,NULL,'Blackhawks vs Canucks',3,0),(206,NULL,'Real Madrid vs Barcelona',3,0),(301,'Beethoven and Brahms','Berlin Philharmonic',1,0),(302,'Unplugged','Eric Clapton',1,0),(303,'Gershwin Rhapsody in Blue','New York Philharmonic',1,0),(304,'Sketches of Spain','Wynton Marsalis',1,0),(305,'The Standard','Take 6',1,0);
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
  KEY `FK_gfkp016vlshfqy1hr15qarmmm` (`acts_id`),
  KEY `FK_events_id_idx` (`events_id`),
  CONSTRAINT `FK_acts_id` FOREIGN KEY (`acts_id`) REFERENCES `acts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_events_id` FOREIGN KEY (`events_id`) REFERENCES `events` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acts_events`
--

LOCK TABLES `acts_events` WRITE;
/*!40000 ALTER TABLE `acts_events` DISABLE KEYS */;
INSERT INTO `acts_events` VALUES (302,501),(302,502),(303,501),(304,501),(305,505),(301,501),(301,502),(301,503),(301,504);
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
  `date_time` datetime DEFAULT CURRENT_TIMESTAMP,
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
INSERT INTO `events` VALUES (1,NULL,NULL,3),(12,NULL,1,1),(13,NULL,8,3),(14,NULL,1,1),(15,NULL,9,4),(16,NULL,1,1),(17,NULL,10,5),(18,NULL,1,1),(19,NULL,11,6),(20,NULL,1,1),(21,NULL,7,2),(22,NULL,1,1),(23,NULL,8,3),(24,NULL,1,1),(25,NULL,9,4),(26,NULL,1,1),(27,NULL,10,5),(28,NULL,1,1),(29,NULL,11,6),(30,NULL,1,1),(31,NULL,7,2),(32,NULL,1,1),(33,NULL,8,3),(34,NULL,1,1),(35,NULL,9,4),(36,NULL,1,1),(37,NULL,10,5),(38,NULL,1,1),(39,NULL,11,6),(40,NULL,1,1),(41,NULL,7,2),(42,NULL,1,1),(43,NULL,8,3),(44,NULL,1,1),(45,NULL,9,4),(46,NULL,1,1),(47,NULL,10,5),(48,NULL,1,1),(49,NULL,11,6),(50,NULL,1,1),(51,NULL,7,2),(63,NULL,1,52),(64,NULL,59,54),(65,NULL,1,52),(66,NULL,60,55),(67,NULL,1,52),(68,NULL,61,56),(69,NULL,1,52),(70,NULL,62,57),(71,NULL,1,52),(72,NULL,58,53),(73,NULL,1,52),(74,NULL,59,54),(75,NULL,1,52),(76,NULL,60,55),(77,NULL,1,52),(78,NULL,61,56),(79,NULL,1,52),(80,NULL,62,57),(81,NULL,1,52),(82,NULL,58,53),(83,NULL,1,52),(84,NULL,59,54),(85,NULL,1,52),(86,NULL,60,55),(87,NULL,1,52),(88,NULL,61,56),(89,NULL,1,52),(90,NULL,62,57),(91,NULL,1,52),(92,NULL,58,53),(93,NULL,1,52),(94,NULL,59,54),(95,NULL,1,52),(96,NULL,60,55),(97,NULL,1,52),(98,NULL,61,56),(99,NULL,1,52),(100,NULL,62,57),(101,NULL,1,52),(102,NULL,58,53),(114,NULL,1,103),(115,NULL,110,105),(116,NULL,1,103),(117,NULL,111,106),(118,NULL,1,103),(119,NULL,112,107),(120,NULL,1,103),(121,NULL,113,108),(122,NULL,1,103),(123,NULL,109,104),(124,NULL,1,103),(125,NULL,110,105),(126,NULL,1,103),(127,NULL,111,106),(128,NULL,1,103),(129,NULL,112,107),(130,NULL,1,103),(131,NULL,113,108),(132,NULL,1,103),(133,NULL,109,104),(134,NULL,1,103),(135,NULL,110,105),(136,NULL,1,103),(137,NULL,111,106),(138,NULL,1,103),(139,NULL,112,107),(140,NULL,1,103),(141,NULL,113,108),(142,NULL,1,103),(143,NULL,109,104),(144,NULL,1,103),(145,NULL,110,105),(146,NULL,1,103),(147,NULL,111,106),(148,NULL,1,103),(149,NULL,112,107),(150,NULL,1,103),(151,NULL,113,108),(152,NULL,1,103),(153,NULL,109,104),(165,NULL,1,154),(166,NULL,161,156),(167,NULL,1,154),(168,NULL,162,157),(169,NULL,1,154),(170,NULL,163,158),(171,NULL,1,154),(172,NULL,164,159),(173,NULL,1,154),(174,NULL,160,155),(175,NULL,1,154),(176,NULL,161,156),(177,NULL,1,154),(178,NULL,162,157),(179,NULL,1,154),(180,NULL,163,158),(181,NULL,1,154),(182,NULL,164,159),(183,NULL,1,154),(184,NULL,160,155),(185,NULL,1,154),(186,NULL,161,156),(187,NULL,1,154),(188,NULL,162,157),(189,NULL,1,154),(190,NULL,163,158),(191,NULL,1,154),(192,NULL,164,159),(193,NULL,1,154),(194,NULL,160,155),(195,NULL,1,154),(196,NULL,161,156),(197,NULL,1,154),(198,NULL,162,157),(199,NULL,1,154),(200,NULL,163,158),(201,NULL,1,154),(202,NULL,164,159),(203,NULL,1,154),(204,NULL,160,155),(501,'2015-12-31 20:00:00',401,NULL),(502,'2016-01-01 20:00:00',401,NULL),(503,'2015-12-31 21:00:00',402,NULL),(504,'2015-12-25 10:00:00',402,NULL),(505,'2016-01-01 10:00:00',402,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES (1,NULL,NULL,NULL,NULL,NULL,NULL,'System','Administrator',NULL),(2,'Springfield','USA','12345','MA','1 Python Place','mike@wxyz.me','Mike','Woinoski',NULL),(3,'Springfield','USA','97478','OR','123 Maple St','marge.simpson@gmail.com','Margret','Simpson','Emily'),(4,'Springfield','USA','97478','OR','123 Maple St','homer.simpson@gmail.com','Homer','Simpson','Virgil'),(7,'New York','USA','10012','NY','342 W 12th St Apt 3C','john.coltrane@gmail.com','John','Coltrane','William'),(8,'New York','USA','10012','NY','342 W 12th St 3D','mccoy.tyner@gmail.com','Alfred','Tyner','McCoy'),(9,'','','','','','dm@gmail.com','Deleteme','Newuser',''),(20,'Springfield','USA','97478','OR','125 Maple St','ned.flanders@gmail.com','Ned','Flanders','Abraham'),(33,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis','Dewey'),(34,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis',NULL),(35,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis','Dewey'),(36,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis',NULL),(37,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis','Dewey'),(38,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis',NULL),(39,'New York','USA','10012','NY','5311 E 1st St','miles@jazz.com','Miles','Davis','Dewey');
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
INSERT INTO `venues` VALUES (1,'New York','US',40.764938,-73.979897,'Carnegie Hall','NY','881 Seventh Avenue'),(2,'Toronto','CA',43.646596,-79.386413,'Roy Thompson Hall','ON','60 Simcoe Street'),(7,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(8,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(9,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(10,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(11,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(58,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(59,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(60,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(61,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(62,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(109,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(110,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(111,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(112,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(113,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(160,NULL,NULL,NULL,NULL,'Rogers Stadium',NULL,NULL),(161,NULL,NULL,NULL,NULL,'Candlestick Park',NULL,NULL),(162,NULL,NULL,NULL,NULL,'Maple Leaf Gardens',NULL,NULL),(163,NULL,NULL,NULL,NULL,'United Centre',NULL,NULL),(164,NULL,NULL,NULL,NULL,'London Palladium',NULL,NULL),(401,'Chicago','USA',41.8369,-87.6847,'Auditorium Theatre','IL','E Congress Pkwy, Chicago, IL 60605'),(402,'New York','USA',40.7127,-74.0059,'Carnegie Hall','NY','881 7th Ave, New York, NY 10019');
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

-- Dump completed on 2015-12-21 17:40:16
