call bucketlist.sp_createUser('hi', 'there', 'guest');

select *
from `BucketList`.`tbl_user`

select IFNULL(wish_id,0)
from `BucketList`.`tbl_wish`


select *
from `tbl_likes`