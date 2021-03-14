"""Update Layer for GNN implementation."""
import tensorflow as _tf

from .input import UpdateInput


class GRUUpdate(_tf.keras.layers.Layer):
    """Update function layer with GRU for GNN model."""

    def __init__(self, hidden_state_size=10, message_size=10, *args, **kwargs):
        super(GRUUpdate, self).__init__(*args, **kwargs)
        self.hidden_state_size = hidden_state_size
        self.message_size = message_size
        # Init inner layers
        self.up = _tf.keras.layers.GRUCell(units=hidden_state_size, name="update-gru")

    def call(self, inputs: UpdateInput, training=None):
        # Flatten batch-nodes
        batch_size = _tf.shape(inputs.hidden)[0]
        num_nodes = _tf.shape(inputs.hidden)[1]
        messages = _tf.reshape(inputs.messages, [batch_size * num_nodes, self.message_size])
        hidden = _tf.reshape(inputs.hidden, [batch_size * num_nodes, self.hidden_state_size])
        # Call update function
        new_hidden, _ = self.up(messages, states=hidden, training=training)
        # Restore batches
        return _tf.reshape(new_hidden, [batch_size, num_nodes, self.hidden_state_size])
