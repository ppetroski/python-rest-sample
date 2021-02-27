DROP TABLE IF EXISTS `trk_Interaction`;
CREATE TABLE `trk_Interaction` (
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL UNIQUE,
  `pid_Profile` int NOT NULL,
  `type` varchar(50) NOT NULL,
  `outcome` varchar(50) NOT NULL,
  `ip_address` varchar(50) NULL,
  `geo_location` JSON DEFAULT NULL, /* Added but not used */
  PRIMARY KEY (`id`),
  FOREIGN KEY (pid_Profile) REFERENCES pid_Profile(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;