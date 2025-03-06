from shadeform.utils import LaunchConfiguration, VolumeConfiguration

def test_docker_launch_config_minimal():
    """Test creating a minimal Docker launch configuration."""
    config = LaunchConfiguration.docker(image="pytorch/pytorch:latest")
    
    assert config == {
        "type": "docker",
        "image": "pytorch/pytorch:latest"
    }

def test_docker_launch_config_full():
    """Test creating a full Docker launch configuration."""
    config = LaunchConfiguration.docker(
        image="pytorch/pytorch:latest",
        command="python train.py",
        env_vars={"BATCH_SIZE": "64", "EPOCHS": "10"},
        ports=[8000, 8080]
    )
    
    assert config == {
        "type": "docker",
        "image": "pytorch/pytorch:latest",
        "command": "python train.py",
        "environment": {"BATCH_SIZE": "64", "EPOCHS": "10"},
        "ports": [8000, 8080]
    }

def test_docker_launch_config_with_env_vars():
    """Test Docker launch configuration with environment variables."""
    config = LaunchConfiguration.docker(
        image="pytorch/pytorch:latest",
        env_vars={"MODEL": "resnet50", "DEVICE": "cuda"}
    )
    
    assert config["type"] == "docker"
    assert config["environment"]["MODEL"] == "resnet50"
    assert config["environment"]["DEVICE"] == "cuda"

def test_docker_launch_config_with_ports():
    """Test Docker launch configuration with ports."""
    config = LaunchConfiguration.docker(
        image="pytorch/pytorch:latest",
        ports=[80, 443, 8080]
    )
    
    assert config["type"] == "docker"
    assert config["ports"] == [80, 443, 8080]

def test_script_launch_config_bash():
    """Test creating a bash script launch configuration."""
    script_content = """#!/bin/bash
    echo "Hello, world!"
    """
    config = LaunchConfiguration.script(content=script_content)
    
    assert config == {
        "type": "script",
        "language": "bash",
        "content": script_content
    }

def test_script_launch_config_python():
    """Test creating a Python script launch configuration."""
    script_content = """
    import torch
    print(f"CUDA available: {torch.cuda.is_available()}")
    """
    config = LaunchConfiguration.script(
        content=script_content,
        language="python"
    )
    
    assert config == {
        "type": "script",
        "language": "python",
        "content": script_content
    }

def test_volume_attachment_config():
    """Test creating a volume attachment configuration."""
    config = VolumeConfiguration.create_attachment(
        volume_id="vol-123",
        mount_path="/data"
    )
    
    assert config == {
        "volume_id": "vol-123",
        "mount_path": "/data"
    }

def test_multiple_volume_attachments():
    """Test creating multiple volume attachment configurations."""
    configs = [
        VolumeConfiguration.create_attachment("vol-123", "/data"),
        VolumeConfiguration.create_attachment("vol-456", "/models")
    ]
    
    assert len(configs) == 2
    assert configs[0]["mount_path"] == "/data"
    assert configs[1]["mount_path"] == "/models"

def test_volume_attachment_absolute_path():
    """Test volume attachment with absolute path."""
    config = VolumeConfiguration.create_attachment(
        volume_id="vol-123",
        mount_path="/absolute/path/to/mount"
    )
    
    assert config["mount_path"].startswith("/")

def test_docker_launch_config_command_list():
    """Test Docker launch configuration with command as list."""
    config = LaunchConfiguration.docker(
        image="pytorch/pytorch:latest",
        command="python -m pytest tests/"
    )
    
    assert config["type"] == "docker"
    assert config["command"] == "python -m pytest tests/"