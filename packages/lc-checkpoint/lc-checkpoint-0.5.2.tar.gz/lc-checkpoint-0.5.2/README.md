# LC-Checkpoint

LC-Checkpoint is a Python package that implements the LC-Checkpoint method for compressing and checkpointing PyTorch models during training.

## Installation

You can install LC-Checkpoint using pip:

```
pip install lc_checkpoint
```

## Usage

To use LC-Checkpoint in your PyTorch training script, you can follow these steps:

1.  Import the LC-Checkpoint module:
    
    ```
    from lc_checkpoint import main as lc
    ```
    

    
2.  Initialize the LC-Checkpoint method with your PyTorch model, optimizer, loss function, and other hyperparameters:
    
    ```
    model = model()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.CrossEntropyLoss()
    checkpoint_dir = 'checkpoints/lc-checkpoint'
    num_buckets = 5
    num_bits = 32

    lc.initialize(model, optimizer, criterion, checkpoint_dir, num_buckets, num_bits)
    ```
    
    
3.  Use the LC-Checkpoint method in your training loop:
    
    ```

    # Save base model weights
    init_save_dir = "checkpoints/initialstate.pt"
    torch.save(model.state_dict(), init_save_dir)
    prev_state_dict = model.state_dict()

    for epoch in range(epochs):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # Load the previous checkpoints if exist
            try:
                # Find the latest checkpoint file
                lc_checkpoint_files = glob.glob(os.path.join('checkpoints/lc-checkpoint', 'lc_checkpoint_epoch*.pt'))
                latest_checkpoint_file = max(lc_checkpoint_files, key=os.path.getctime)
                prev_state_dict, epoch_loaded = lc.load_checkpoint(latest_checkpoint_file)
                print('Restored latest checkpoint:', latest_checkpoint_file)
                latest_checkpoint_file_size = os.path.getsize(latest_checkpoint_file)
                latest_checkpoint_file_size_kb = latest_checkpoint_file_size / 1024
                print('Latest checkpoint file size:', latest_checkpoint_file_size_kb, 'KB')
                restore_time = time.time() - start_time
                total_restore_time += restore_time
                print('Time taken to restore checkpoint:', restore_time)
                start_time = time.time()  # reset the start time
                print('-' * 50)
            except:
                pass

            # Get the inputs and labels
            inputs, labels = data

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            new_state_dict = model.state_dict()
            new_state_weights = np.concatenate([tensor.numpy().flatten() for tensor in new_state_dict.values()])  # convert each tensor to a numpy array and concatenate them
            prev_state_weights = np.concatenate([tensor.numpy().flatten() for tensor in prev_state_dict.values()])  # convert each tensor to a numpy array and concatenate them
            δt = new_state_weights - prev_state_weights # Get delta
            prev_state_dict = new_state_dict

            # Save the checkpoint
            compressed_data, encoder = lc.compress_data(δt, num_bits=num_bits, k=num_buckets)
            save_start_time = time.time()  # record the start time
            lc.save_checkpoint('checkpoint.pt', compressed_data, epoch, i, encoder)
            save_time = time.time() - save_start_time  # calculate the time taken to save the checkpoint

            # Print statistics
            running_loss += loss.item()
            if i % 1 == 0:    # print every 1 mini-batches
                print('[Epoch: %d, Iteration: %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 1))
                running_loss = 0.0
                print('Time taken to save checkpoint:', save_time)
    ```
4. Using LC-Checkpoint to restore model.
```
last_epoch, last_iter = 30, 8
max_iter = 10
restored_model = restore_model(model(), last_epoch, last_iter, max_iter, init_save_dir)
```

## API Reference

### `lc.initialize(model, optimizer, criterion, checkpoint_dir, num_buckets, num_bits)`

Initializes the LC-Checkpoint method with the given PyTorch model, optimizer, loss function, checkpoint directory, number of buckets, and number of bits.

### `lc.compress_data(δt, num_bits=num_bits, k=num_buckets, treshold=True)`

Compresses the model parameters and returns the compressed data.

### `lc.decode_data(encoded)`

Decodes the compressed data and returns the original model parameters.

### `lc.save_checkpoint(filename, compressed_data, epoch, iteration)`

Saves the compressed data to a file with the given filename, epoch, and iteration.

### `lc.load_checkpoint(filename)`

Loads the compressed data from a file with the given filename.

### `lc.restore_model(model, last_epoch, last_iter, max_iter, init_filename, ckpt_name)`
Loads the compressed data into a pytorch model.

### `lc.restore_model_async(model, last_epoch, last_iter, max_iter, init_filename, ckpt_name, n_cores)`
Loads the compressed data into a pytorch model asynchronously.

### `lc.calculate_compression_rate(prev_state_dict, num_bits=num_bits, num_buckets=num_buckets)`

Calculates the compression rate of the LC-Checkpoint method based on the previous state dictionary and the current number of bits and buckets.

## License

LC-Checkpoint is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgements

LC-Checkpoint is based on paper "On Efficient Constructions of Checkpoints" authored by Yu Chen, Zhenming Liu, Bin Ren, Xin Jin.