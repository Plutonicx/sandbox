CREATE DATABASE BucketList;


DROP TABLE `BucketList`.`tbl_user`

CREATE TABLE `BucketList`.`tbl_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(255) NULL,
  `user_username` VARCHAR(255) NULL,
  `user_password` VARCHAR(4000) NULL,
  PRIMARY KEY (`user_id`));
  

DROP PROCEDURE `sp_createUser`

  DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(255),
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(4000)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(255)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;




CREATE TABLE `tbl_wish` (
  `wish_id` int(11) NOT NULL AUTO_INCREMENT,
  `wish_title` varchar(255) DEFAULT NULL,
  `wish_description` varchar(5000) DEFAULT NULL,
  `wish_user_id` int(11) DEFAULT NULL,
  `wish_date` datetime DEFAULT NULL,
  PRIMARY KEY (`wish_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;


USE `BucketList`;
DROP procedure IF EXISTS `BucketList`.`sp_addWish`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish`(
    IN p_title varchar(255),
    IN p_description varchar(4500),
    IN p_user_id bigint
)
BEGIN
    insert into tbl_wish(
        wish_title,
        wish_description,
        wish_user_id,
        wish_date
    )
    values
    (
        p_title,
        p_description,
        p_user_id,
        NOW()
    );
END$$
 
DELIMITER ;
;

USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;
 
DELIMITER $$
USE `BucketList`$$
CREATE PROCEDURE `sp_GetWishByUser` (
IN p_user_id bigint
)
BEGIN
    select * from tbl_wish where wish_user_id = p_user_id;
END$$
 
DELIMITER ;




DELIMITER $$
 
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishById`(
IN p_wish_id bigint,
In p_user_id bigint
)
BEGIN
select * from tbl_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END



DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish`(
IN p_title varchar(255),
IN p_description varchar(4000),
IN p_wish_id bigint,
In p_user_id bigint
)
BEGIN
update tbl_wish set wish_title = p_title,wish_description = p_description
    where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$
DELIMITER ;


DELIMITER $$
USE `BucketList`$$
CREATE PROCEDURE `sp_deleteWish` (
IN p_wish_id bigint,
IN p_user_id bigint
)
BEGIN
delete from tbl_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$
 
DELIMITER ;

USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishByUser`(
IN p_user_id bigint,
IN p_limit int,
IN p_offset int
)
BEGIN
    SET @t1 = CONCAT( 'select * from tbl_wish where wish_user_id = ', p_user_id, ' order by wish_date desc limit ',p_limit,' offset ',p_offset);
    PREPARE stmt FROM @t1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt1;
END$$
 
DELIMITER ;


USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishByUser`(
IN p_user_id bigint,
IN p_limit int,
IN p_offset int,
out p_total bigint
)
BEGIN
     
    select count(*) into p_total from tbl_wish where wish_user_id = p_user_id;
 
    SET @t1 = CONCAT( 'select * from tbl_wish where wish_user_id = ', p_user_id, ' order by wish_date desc limit ',p_limit,' offset ',p_offset);
    PREPARE stmt FROM @t1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$
 
DELIMITER ;



ALTER TABLE `BucketList`.`tbl_wish` 
ADD COLUMN `wish_file_path` VARCHAR(400) NULL AFTER `wish_date`,
ADD COLUMN `wish_accomplished` INT NULL DEFAULT 0 AFTER `wish_file_path`,
ADD COLUMN `wish_private` INT NULL DEFAULT 0 AFTER `wish_accomplished`;


USE `BucketList`;
DROP procedure IF EXISTS `sp_addWish`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish`(
    IN p_title varchar(45),
    IN p_description varchar(4000),
    IN p_user_id bigint,
    IN p_file_path varchar(400),
    IN p_is_private int,
    IN p_is_done int
)
BEGIN
    insert into tbl_wish(
        wish_title,
        wish_description,
        wish_user_id,
        wish_date,
        wish_file_path,
        wish_private,
        wish_accomplished
    )
    values
    (
        p_title,
        p_description,
        p_user_id,
        NOW(),
        p_file_path,
        p_is_private,
        p_is_done
    );
END$$
 
DELIMITER ;


USE `BucketList`;
DROP procedure IF EXISTS `sp_updateWish`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish`(
IN p_title varchar(45),
IN p_description varchar(4000),
IN p_wish_id bigint,
In p_user_id bigint,
IN p_file_path varchar(400),
IN p_is_private int,
IN p_is_done int
)
BEGIN
update tbl_wish set
    wish_title = p_title,
    wish_description = p_description,
    wish_file_path = p_file_path,
    wish_private = p_is_private,
    wish_accomplished = p_is_done
    where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$
 
DELIMITER ;

USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishById`;

DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishById`(
IN p_wish_id bigint,
In p_user_id bigint
)
BEGIN
	select wish_id,wish_title,wish_description,wish_file_path,wish_private,wish_accomplished from tbl_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$

DELIMITER ;

USE `BucketList`;
DROP procedure IF EXISTS `sp_updateWish`;


DELIMITER $$
 
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish`(
IN p_title varchar(45),
IN p_description varchar(4000),
IN p_wish_id bigint,
In p_user_id bigint,
IN p_file_path varchar(400),
IN p_is_private int,
IN p_is_done int
)
BEGIN
update tbl_wish set
    wish_title = p_title,
    wish_description = p_description,
    wish_file_path = p_file_path,
    wish_private = p_is_private,
    wish_accomplished = p_is_done
    where wish_id = p_wish_id and wish_user_id = p_user_id;
END


USE `BucketList`;
DROP procedure IF EXISTS `sp_GetAllWishes`;
 
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAllWishes`()
BEGIN
    select wish_id,wish_title,wish_description,wish_file_path from tbl_wish where wish_private = 0;
END$$
 
DELIMITER ;

