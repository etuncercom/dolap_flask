-- MariaDB dump 10.17  Distrib 10.4.11-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: dolap
-- ------------------------------------------------------
-- Server version	10.4.11-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dolap`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dolap` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `dolap`;

--
-- Table structure for table `begenilen_urunler`
--

DROP TABLE IF EXISTS `begenilen_urunler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `begenilen_urunler` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `urun_id` varchar(45) DEFAULT NULL,
  `hesap_id` int(11) DEFAULT NULL,
  `begenme_tarih` datetime DEFAULT NULL,
  `islem` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4184 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bot_hesaplar`
--

DROP TABLE IF EXISTS `bot_hesaplar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bot_hesaplar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hesap_adi` varchar(200) DEFAULT NULL,
  `hesap_sifre` varchar(200) DEFAULT NULL,
  `hesap_mail` varchar(200) DEFAULT NULL,
  `dolap_id` int(11) DEFAULT NULL,
  `dolap_takip_eden` varchar(45) DEFAULT NULL,
  `dolap_takip_ettigi` varchar(45) DEFAULT NULL,
  `atoken` varchar(100) DEFAULT NULL,
  `kullanici_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hesaplar`
--

DROP TABLE IF EXISTS `hesaplar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hesaplar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hesap_adi` varchar(45) DEFAULT NULL,
  `hesap_sifre` varchar(45) DEFAULT NULL,
  `hesap_mail` varchar(45) DEFAULT NULL,
  `dolap_id` int(11) DEFAULT NULL,
  `dolap_takip_eden` varchar(45) DEFAULT NULL,
  `dolap_takip_ettigi` varchar(45) DEFAULT NULL,
  `atoken` varchar(100) DEFAULT NULL,
  `kullanici_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kullanicilar`
--

DROP TABLE IF EXISTS `kullanicilar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kullanicilar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `kadi` varchar(45) DEFAULT NULL,
  `sifre` varchar(45) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `kayit_tarih` datetime DEFAULT NULL,
  `giris_tarih` datetime DEFAULT NULL,
  `onay` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `one_cikanlar`
--

DROP TABLE IF EXISTS `one_cikanlar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `one_cikanlar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `urun_id` int(11) DEFAULT NULL,
  `hesap_id` int(11) DEFAULT NULL,
  `cikarma_tarih` datetime DEFAULT NULL,
  `cikarma_bitis_tarih` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `onerilen_hesaplar`
--

DROP TABLE IF EXISTS `onerilen_hesaplar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `onerilen_hesaplar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `hesap_id` int(11) DEFAULT NULL,
  `onerilen_dolap_id` int(11) DEFAULT NULL,
  `onerme_tarih` datetime DEFAULT NULL,
  `onerme_bitis_tarih` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `urunlerim`
--

DROP TABLE IF EXISTS `urunlerim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `urunlerim` (
  `ID` int(11) NOT NULL,
  `Baslik` varchar(50) DEFAULT NULL,
  `Foto` varchar(255) DEFAULT NULL,
  `Begeni` varchar(45) DEFAULT NULL,
  `Yorum` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-18 14:43:56
