CREATE TABLE `alert` (
  `regionName` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `alertLevel` int NOT NULL,
  PRIMARY KEY (`regionName`,`date`),
  KEY `alertLevel_fk` (`alertLevel`),
  CONSTRAINT `alertLevel_fk` FOREIGN KEY (`alertLevel`) REFERENCES `alertDetails` (`alertLevel`),
  CONSTRAINT `alertRegionName_fk` FOREIGN KEY (`regionName`) REFERENCES `region` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `alertDetails` (
  `alertLevel` int NOT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `prompt` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `measures` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`alertLevel`),
  UNIQUE KEY `alertLevel_UNIQUE` (`alertLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `city` (
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `regionName` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`name`),
  KEY `regionName_fk` (`regionName`),
  CONSTRAINT `regionName_fk` FOREIGN KEY (`regionName`) REFERENCES `region` (`name`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `cityPostalCodeMapping` (
  `city` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `postalCodeRegion` char(3) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`postalCodeRegion`),
  UNIQUE KEY `postalCodeRegion_UNIQUE` (`postalCodeRegion`),
  KEY `city` (`city`),
  CONSTRAINT `city_fk` FOREIGN KEY (`city`) REFERENCES `city` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `currentDate` (
  `date` date NOT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Used to simulate date';


CREATE TABLE `diagnostic` (
  `testID` int unsigned NOT NULL AUTO_INCREMENT,
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `publicHealthWorkerID` int NOT NULL,
  `publicHealthCenterID` int NOT NULL,
  `testDate` date NOT NULL,
  `resultDate` date NOT NULL,
  `result` tinyint(1) NOT NULL,
  PRIMARY KEY (`testID`),
  UNIQUE KEY `testID_UNIQUE` (`testID`),
  KEY `id_idx` (`publicHealthCenterID`),
  KEY `workerID_idx` (`publicHealthWorkerID`),
  KEY `medicareNumber` (`medicareNumber`),
  CONSTRAINT `medicareNumber` FOREIGN KEY (`medicareNumber`) REFERENCES `person` (`medicareNumber`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `followUpForm` (
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `temperature` float NOT NULL,
  `fever` tinyint(1) NOT NULL DEFAULT '0',
  `cough` tinyint(1) NOT NULL DEFAULT '0',
  `shortnessOfBreath` tinyint(1) NOT NULL DEFAULT '0',
  `lossOfTaste` tinyint(1) NOT NULL DEFAULT '0',
  `nausea` tinyint(1) NOT NULL DEFAULT '0',
  `stomachAche` tinyint(1) NOT NULL DEFAULT '0',
  `diarrhea` tinyint(1) NOT NULL DEFAULT '0',
  `vomiting` tinyint(1) NOT NULL DEFAULT '0',
  `headache` tinyint(1) NOT NULL DEFAULT '0',
  `musclePain` tinyint(1) NOT NULL DEFAULT '0',
  `soreThroat` tinyint(1) NOT NULL DEFAULT '0',
  `otherSymptomes` varchar(255) COLLATE utf8_unicode_ci DEFAULT '0',
  PRIMARY KEY (`medicareNumber`,`date`),
  CONSTRAINT `medicareNumber_fk` FOREIGN KEY (`medicareNumber`) REFERENCES `person` (`medicareNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `groupZone` (
  `groupID` int unsigned NOT NULL AUTO_INCREMENT,
  `groupName` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`groupID`),
  UNIQUE KEY `groupID_UNIQUE` (`groupID`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `groupZoneMapping` (
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `groupID` int unsigned NOT NULL,
  PRIMARY KEY (`medicareNumber`,`groupID`),
  KEY `groupZone_idx` (`groupID`),
  CONSTRAINT `groupZone` FOREIGN KEY (`groupID`) REFERENCES `groupZone` (`groupID`) ON UPDATE CASCADE,
  CONSTRAINT `groupZoneMedicareNumber` FOREIGN KEY (`medicareNumber`) REFERENCES `person` (`medicareNumber`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `healthRecommendation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mainInstruction` varchar(1000) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `mainInstruction_UNIQUE` (`mainInstruction`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `healthRecommendationSecondary` (
  `id` int NOT NULL,
  `recommendation` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`,`recommendation`),
  CONSTRAINT `id_fk` FOREIGN KEY (`id`) REFERENCES `healthRecommendation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `region` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `oldAlertLevel` int DEFAULT NULL,
  `newAlertLevel` int DEFAULT NULL,
  `healthRecommendation` varchar(700) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `testResult` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `messageMedicareNumber_fk` (`medicareNumber`),
  CONSTRAINT `messageMedicareNumber_fk` FOREIGN KEY (`medicareNumber`) REFERENCES `person` (`medicareNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `person` (
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `firstName` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `lastName` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `dateOfBirth` date NOT NULL,
  `phoneNumber` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `province` char(2) COLLATE utf8_unicode_ci NOT NULL,
  `postalCode` char(6) COLLATE utf8_unicode_ci NOT NULL,
  `country` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `citizenship` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `motherMedicare` char(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fatherMedicare` char(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`medicareNumber`),
  UNIQUE KEY `medicareNumber_UNIQUE` (`medicareNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `publicHealthCenter` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `webAddress` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `phoneNumber` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `type` enum('hospital','clinic','special_installment') COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `province` char(2) COLLATE utf8_unicode_ci NOT NULL,
  `country` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `postalCode` char(6) COLLATE utf8_unicode_ci NOT NULL,
  `testingType` enum('appointment','walk-in','both') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'both',
  `driveThru` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `publicHealthWorker` (
  `workerID` int unsigned NOT NULL AUTO_INCREMENT,
  `medicareNumber` char(12) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`workerID`),
  UNIQUE KEY `workerID_UNIQUE` (`workerID`),
  UNIQUE KEY `medicareNumber_UNIQUE` (`medicareNumber`),
  CONSTRAINT `workerMedicareNumber` FOREIGN KEY (`medicareNumber`) REFERENCES `person` (`medicareNumber`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `region` (
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `workerHealthCenterMapping` (
  `healthWorkerID` int unsigned NOT NULL,
  `healthCenterID` int unsigned NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date DEFAULT NULL,
  PRIMARY KEY (`healthWorkerID`,`healthCenterID`),
  KEY `healthCenter_fk_idx` (`healthCenterID`),
  CONSTRAINT `healthCenter_fk` FOREIGN KEY (`healthCenterID`) REFERENCES `publicHealthCenter` (`id`),
  CONSTRAINT `healthWorker_fk` FOREIGN KEY (`healthWorkerID`) REFERENCES `publicHealthWorker` (`workerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `workerSchedule` (
  `workerID` int NOT NULL,
  `date` date NOT NULL,
  `shift` enum('morning','day','evening','night') COLLATE utf8_unicode_ci NOT NULL,
  `healthCenterID` int NOT NULL,
  PRIMARY KEY (`workerID`,`date`,`healthCenterID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
