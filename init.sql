-- Users 테이블
CREATE TABLE users (
    uuid UUID PRIMARY KEY,
    user_id VARCHAR(30) NOT NULL,
    user_pw VARCHAR(60) NOT NULL,
    user_nm VARCHAR(30) NOT NULL,
    user_email VARCHAR(50) NOT NULL,
    create_dt DATE default current_timestamp,
    delete_dt DATE,
    isDelete BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_user_id UNIQUE (user_id)     -- user_id는 고유값 보장
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
COMMENT ON COLUMN users.isDelete IS '삭제 여부 플래그';


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
    isComplete BOOLEAN DEFAULT FALSE,
    isDelete BOOLEAN DEFAULT FALSE,
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
COMMENT ON COLUMN stamps.isComplete IS '완료 여부 플래그';
COMMENT ON COLUMN stamps.isDelete IS '삭제 여부 플래그';


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