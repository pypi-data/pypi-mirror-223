module grpc_client_go

go 1.19

require (
	google.golang.org/grpc v1.50.0
	google.golang.org/protobuf v1.28.1 // indirect
)

require github.com/bentoml/bentoml/grpc/v1alpha1 v0.0.0-unpublished

replace github.com/bentoml/bentoml/grpc/v1alpha1 v0.0.0-unpublished => ./github.com/bentoml/bentoml/grpc/v1alpha1

require (
	github.com/golang/protobuf v1.5.2 // indirect
	golang.org/x/net v0.0.0-20201021035429-f5854403a974 // indirect
	golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4 // indirect
	golang.org/x/text v0.3.3 // indirect
	google.golang.org/genproto v0.0.0-20200526211855-cb27e3aa2013 // indirect
)
