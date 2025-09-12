-- Users 테이블
CREATE TABLE users (
    uuid UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    user_pw VARCHAR(60) NOT NULL,
    user_nm VARCHAR(30) NOT NULL,
    user_email VARCHAR(50) NOT NULL,
    create_dt DATE default current_timestamp,
    delete_dt DATE,
    is_delete BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_user_id UNIQUE (user_id) ,    -- user_id는 고유값 보장
    CONSTRAINT uq_user_email UNIQUE (user_email)     -- user_email은 고유값 보장
);

COMMENT ON TABLE users IS '사용자 계정 테이블';
COMMENT ON COLUMN users.uuid IS 'PK, 자동 증가';
COMMENT ON COLUMN users.user_id IS '사용자 로그인 ID';
COMMENT ON COLUMN users.user_pw IS '비밀번호';
COMMENT ON COLUMN users.user_nm IS '사용자 이름';
COMMENT ON COLUMN users.user_email IS '이메일';
COMMENT ON COLUMN users.create_dt IS '생성일';
COMMENT ON COLUMN users.delete_dt IS '삭제일';
COMMENT ON COLUMN users.is_delete IS '삭제 여부 플래그';


-- Stamps 테이블
CREATE TABLE stamps (
    stamp_id UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    stamp_nm VARCHAR(100) NOT NULL,
    stamp_desc VARCHAR(200),
    stamp_type VARCHAR(10),
    total_cnt INT NOT NULL,
    progress_cnt INT DEFAULT 0,
    create_dt DATE default current_timestamp,
    modify_dt DATE,
    complete_dt DATE,
    delete_dt DATE,
    is_complete BOOLEAN DEFAULT FALSE,
    is_delete BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_stamp_user FOREIGN KEY (user_id) REFERENCES "users"(user_id)
);

COMMENT ON TABLE stamps IS '스탬프(달성표) 테이블';
COMMENT ON COLUMN stamps.stamp_id IS 'PK, 자동 증가';
COMMENT ON COLUMN stamps.user_id IS 'FK, users.user_id';
COMMENT ON COLUMN stamps.stamp_nm IS '스탬프 이름';
COMMENT ON COLUMN stamps.stamp_desc IS '스탬프 설명';
COMMENT ON COLUMN stamps.stamp_type IS '스탬프 타입';
COMMENT ON COLUMN stamps.total_cnt IS '총 개수';
COMMENT ON COLUMN stamps.progress_cnt IS '진행 개수';
COMMENT ON COLUMN stamps.create_dt IS '생성일';
COMMENT ON COLUMN stamps.modify_dt IS '수정일';
COMMENT ON COLUMN stamps.complete_dt IS '완료일';
COMMENT ON COLUMN stamps.delete_dt IS '삭제일';
COMMENT ON COLUMN stamps.is_complete IS '완료 여부 플래그';
COMMENT ON COLUMN stamps.is_delete IS '삭제 여부 플래그';

-- SystemLogs 테이블
CREATE TABLE system_logs (
    log_id UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    log_type VARCHAR(10) NOT NULL,
    log_desc text NOT NULL,
    log_date DATE default current_timestamp,
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES "users"(user_id)
);

COMMENT ON TABLE system_logs IS '시스템 로그 테이블';
COMMENT ON COLUMN system_logs.log_id IS 'PK, 자동 증가';
COMMENT ON COLUMN system_logs.user_id IS 'FK, users.user_id';
COMMENT ON COLUMN system_logs.log_type IS '로그 타입 (예: LOGIN, ERROR 등)';
COMMENT ON COLUMN system_logs.log_desc IS '비고';
COMMENT ON COLUMN system_logs.log_date IS '로그 발생 일자';

/**
*   2025.08.31  - 스탬프 이미지 테이블 및 stamps 테이블 이미지 컬럼 추가
*
*/
-- stame_images 테이블 
CREATE TABLE stamp_images (
    image_id UUID PRIMARY KEY,
    image_key TEXT NOT NULL,
    is_public BOOLEAN DEFAULT TRUE,
    user_id VARCHAR(30),
    create_dt DATE default current_timestamp,
    is_delete BOOLEAN DEFAULT FALSE,
    delete_dt DATE,
    image_type VARCHAR(10) NOT NULL,
    CONSTRAINT fk_image_user FOREIGN KEY (user_id) REFERENCES "users"(user_id)
);

COMMENT ON TABLE stamp_images IS '스탬프 이미지 테이블';
COMMENT ON COLUMN stamp_images.image_key IS 'PK, 자동 증가';
COMMENT ON COLUMN stamp_images.image_key IS '이미지 URL(S3 또는 MinIO 경로)';
COMMENT ON COLUMN stamp_images.is_public IS '공개 여부 플래그';
COMMENT ON COLUMN stamp_images.user_id IS 'FK, users.user_id: 유저 전용일 시 사용';
COMMENT ON COLUMN stamp_images.create_dt IS '업로드 일자';
COMMENT ON COLUMN stamp_images.is_delete IS '삭제 여부 플래그';
COMMENT ON COLUMN stamp_images.delete_dt IS '삭제 일자';
COMMENT ON COLUMN stamp_images.image_type IS '이미지 유형(before, after)';

ALTER TABLE stamps ADD COLUMN before_image_id UUID;
ALTER TABLE stamps ADD COLUMN after_image_id UUID;

ALTER TABLE stamps ADD CONSTRAINT fk_before_image FOREIGN KEY (before_image_id) REFERENCES stamp_images(image_id);
ALTER TABLE stamps ADD CONSTRAINT fk_after_image FOREIGN KEY (after_image_id) REFERENCES stamp_images(image_id);

ALTER TABLE stamp_images ADD CONSTRAINT uq_image_key UNIQUE (image_key);  -- image_key는 고유값 보장

/**
*   2025.09.08 친구 테이블 추가 
*
*/
CREATE TABLE friends (
    friend_id UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    friend_user_id VARCHAR(30) NOT NULL,
    friend_status VARCHAR(10) DEFAULT 'PENDING', -- PENDING, ACCEPTED, REJECTED
    create_dt DATE default current_timestamp,
    delete_dt DATE,
    is_delete BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_friend_user FOREIGN KEY (user_id) REFERENCES "users"(user_id),
    CONSTRAINT fk_friend_friend_user FOREIGN KEY (friend_user_id) REFERENCES "users"(user_id)
);
COMMENT ON TABLE friends IS '친구 관계 테이블';
COMMENT ON COLUMN friends.friend_id IS 'PK, 자동 증가';
COMMENT ON COLUMN friends.user_id IS 'FK, users.user_id: 친구 요청을 보낸 사용자';
COMMENT ON COLUMN friends.friend_user_id IS 'FK, users.user_id: 친구 요청을 받은 사용자';
COMMENT ON COLUMN friends.friend_status IS '친구 상태 (PENDING, ACCEPTED, REJECTED)';
COMMENT ON COLUMN friends.create_dt IS '생성일';
COMMENT ON COLUMN friends.delete_dt IS '삭제일';
COMMENT ON COLUMN friends.is_delete IS '삭제 여부 플래그';
ALTER TABLE friends ADD CONSTRAINT uq_friend UNIQUE (user_id, friend_user_id);  -- user_id와 friend_user_id 조합은 고유값 보장
-- 친구 요청 인덱스
CREATE INDEX idx_friend_user_id ON friends(user_id);
CREATE INDEX idx_friend_friend_user_id ON friends(friend_user_id);

create table notices (
    notice_id UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    notice_type VARCHAR(20) NOT NULL,
    notice_message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_send BOOLEAN DEFAULT FALSE,
    is_delete BOOLEAN DEFAULT FALSE,
    create_dt DATE default current_timestamp,
    read_dt DATE,
    delete_dt DATE,
    CONSTRAINT fk_notice_user FOREIGN KEY (user_id) REFERENCES "users"(user_id)
);
COMMENT ON TABLE notices IS '알림 테이블';
COMMENT ON COLUMN notices.notice_id IS 'PK, 자동 증가';
COMMENT ON COLUMN notices.user_id IS 'FK, users.user_id: 알림 대상 유저';
COMMENT ON COLUMN notices.notice_type IS '알림 타입';
COMMENT ON COLUMN notices.notice_message IS '알림 메시지';
COMMENT ON COLUMN notices.is_read IS '읽음 여부';
COMMENT ON COLUMN notices.is_send IS '발송 여부';
COMMENT ON COLUMN notices.is_delete IS '삭제 여부';
COMMENT ON COLUMN notices.create_dt IS '생성일';
COMMENT ON COLUMN notices.read_dt IS '읽은 일자';
COMMENT ON COLUMN notices.delete_dt IS '삭제 일자';

CREATE INDEX idx_notice_user_id ON notices(user_id);

ALTER TABLE notices ADD COLUMN notice_target VARCHAR(30);
COMMENT ON COLUMN notices.notice_target IS '알림 대상 (예: 친구 요청을 보낸 사용자 ID)';