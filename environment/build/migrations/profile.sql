DROP TABLE IF EXISTS `pid_Profile`;
CREATE TABLE `pid_Profile` (
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL UNIQUE,
  `first_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(25) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address1` varchar(100) DEFAULT NULL,
  `address2` varchar(100) DEFAULT NULL,
  `locality` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,   /* This would normally an INT relation to an xref table */
  `postcode` varchar(25) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,  /* I do this long to capture international and various formats */
  `mobile` varchar(20) DEFAULT NULL, /* I do this long to capture international and various formats */
  `geo_location` JSON DEFAULT NULL, /* JSON object for provider flexibility */
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;