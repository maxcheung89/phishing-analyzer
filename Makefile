# Run this Makefile with: make <target>

# 🔐 Encrypt .env manually (optional, no longer required)
env:
	@python3 backend/encrypt_key.py

# 🧱 Build the Docker image
build:
	docker build -t phishing-analyzer -f Dockerfile .

# 🚀 Run the Flask app with proper tshark capabilities
run:
	docker run --rm -p 5000:5000 \
		--cap-add=NET_RAW --cap-add=NET_ADMIN \
		-v $(PWD)/backend/static/results:/app/static/results \
		--env-file .env phishing-analyzer

# 🧼 Stop and prune all containers and images
clean:
	docker container prune -f
	docker image prune -af

# 🔁 Full reset (Docker cleanup + env reset)
reset:
	rm -f secrets/.key.enc
	make clean
