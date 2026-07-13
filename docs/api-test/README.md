## API 테스트

- 절대 서버를 직접 띄우지 않는다.
- 로컬에서 서버가 실행 중이지 않을 경우, 로컬 서버를 실행해달라고 요청한다.
- pwsh 기준, `netstat -ano | findstr :8000` 또는 `Get-NetTCPConnection -LocalPort 8000`로 서버가 실행중인지 확인한다.
- bash 기준, `ss -tulnp | grep :8000` 로 서버가 실행중인지 확인한다.
- curl로 응답을 확인해야 할 경우 `curl -I http://localhost:8000`로 요청한다.

## API 테스트 결과 작성

[test_template.md](result/test_template.md)를 보고 테스트 결과를 작성한다.

테스트가 실패할 경우 실패로 기록 후, 수정한 뒤 다시 테스트한다. 다시 테스트한 후 기존 파일을 수정하지 않고 새 파일을 작성한다.

## http 파일 작성

`[http](docs/api-test/http)` 폴더에 자원(resource) 별로 파일을 작성한다.

예시 파일) [example.http](http/example.http)