/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- unplj 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `fakenews` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE 'fakenews';

-- 테이블 unplj.annotations 구조 내보내기
CREATE TABLE IF NOT EXISTS `annotations` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `annotator` int(11) unsigned NOT NULL,
  `article_id` int(11) unsigned NOT NULL,
  `atime` timestamp NULL DEFAULT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `count_annotator` (`annotator`)
) ENGINE=InnoDB AUTO_INCREMENT=11601 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.
-- 테이블 unplj.annotators 구조 내보내기
CREATE TABLE IF NOT EXISTS `annotators` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` char(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8;


-- 내보낼 데이터가 선택되어 있지 않습니다.
-- 테이블 unplj.tweets 구조 내보내기
CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `article_id` char(40) NOT NULL DEFAULT '',
  `title` char(60) NOT NULL DEFAULT '',
  `time` char(40) NOT NULL DEFAULT '',
  `company_code` int(11) NOT NULL DEFAULT 0,
  `annotated` int(11) unsigned NOT NULL DEFAULT '0',
  `final_answer` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15405 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
