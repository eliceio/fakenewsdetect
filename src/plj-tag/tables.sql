/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- unplj 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `unplj` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `unplj`;

-- 테이블 unplj.annotations 구조 내보내기
CREATE TABLE IF NOT EXISTS `annotations` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `annotator` int(11) unsigned NOT NULL,
  `tweet_id` int(11) unsigned NOT NULL,
  `atime` timestamp NULL DEFAULT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `count_annotator` (`annotator`)
) ENGINE=InnoDB AUTO_INCREMENT=11601 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.
-- 테이블 unplj.annotations_keywords 구조 내보내기
CREATE TABLE IF NOT EXISTS `annotations_keywords` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `annotator` int(11) unsigned NOT NULL,
  `keyword_id` int(11) unsigned NOT NULL,
  `atime` timestamp NULL DEFAULT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `count_annotator` (`annotator`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
CREATE TABLE IF NOT EXISTS `tweets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` bigint(11) unsigned NOT NULL,
  `username` char(20) NOT NULL DEFAULT '',
  `userid` char(20) NOT NULL DEFAULT '',
  `tweet` char(160) NOT NULL DEFAULT '',
  `time` char(40) NOT NULL DEFAULT '',
  `source_type` int(11) NOT NULL,
  `annotated` int(11) unsigned NOT NULL DEFAULT '0',
  `final_answer` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_id_userid` (`tweet_id`,`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=15405 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
